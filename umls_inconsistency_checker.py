"""
UMLS Inconsistency Checker
Detects Parent-Child Loops and Broader-Than Violations in MRREL.RRF
"""

import argparse
import logging
import csv
import time
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path

import networkx as nx
from tqdm import tqdm

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("umls_analysis.log")],
)
logger = logging.getLogger(__name__)


# Parse MRREL.RRF file and extract edges
def parse_mrrel(file_path):
    parent_child_edges = set()
    broader_than_edges = set()
    duplicate_edges = Counter()
    self_loops = set()
    relationship_types = set()

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"UMLS file not found: {file_path}")

    total_lines = sum(1 for _ in open(file_path, "r", encoding="utf-8"))

    with open(file_path, "r", encoding="utf-8") as f:
        for line in tqdm(f, total=total_lines, desc="Parsing MRREL.RRF"):
            parts = line.strip().split("|")
            if len(parts) < 5:
                continue

            source = parts[0].strip()
            relation = parts[3].strip()
            target = parts[4].strip()

            relationship_types.add(relation)

            if source == target:
                self_loops.add((source, relation))
                continue

            edge = (source, target)

            if relation == "CHD":
                edge = (target, source)
                parent_child_edges.add(edge)
                duplicate_edges[edge] += 1
            elif relation == "PAR":
                parent_child_edges.add(edge)
                duplicate_edges[edge] += 1
            elif relation == "RB":
                broader_than_edges.add(edge)
                duplicate_edges[edge] += 1
            elif relation == "RN":
                edge = (target, source)
                broader_than_edges.add(edge)
                duplicate_edges[edge] += 1

    return parent_child_edges, broader_than_edges, duplicate_edges, self_loops, relationship_types


# Cycle detection using DFS with deduplication
def detect_cycles(graph):
    visited = set()
    rec_stack = set()
    all_cycles = []
    unique_cycles = set()

    def dfs(node, path):
        if node in rec_stack:
            cycle_start = path.index(node)
            cycle = path[cycle_start:]
            normalized = tuple(sorted(cycle))
            if normalized not in unique_cycles:
                unique_cycles.add(normalized)
                all_cycles.append(cycle)
            return

        if node in visited:
            return

        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph[node]:
            dfs(neighbor, path)

        path.pop()
        rec_stack.remove(node)

    for node in list(graph):  # Fixed here to avoid modifying dict during iteration
        if node not in visited:
            dfs(node, [])

    return all_cycles


# Detect broader-than violations
def detect_broader_violations(graph):
    violations = []
    descendants = {node: set(nx.descendants(graph, node)) for node in graph.nodes}

    for src in graph:
        for dst in descendants[src]:
            if src in descendants.get(dst, set()):
                path_fwd = nx.shortest_path(graph, src, dst)
                path_back = nx.shortest_path(graph, dst, src)
                violations.append({
                    "source": src,
                    "target": dst,
                    "cycle": path_fwd + path_back[1:]
                })

    return violations


# Save CSV reports
def save_results(cycles, violations, duplicates, self_loops, stats, output_dir="./res"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if cycles:
        with open(f"{output_dir}/parent_child_cycles_{timestamp}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Cycle_ID", "Cycle"])
            for i, c in enumerate(cycles, 1):
                writer.writerow([i, " -> ".join(c)])

    if violations:
        with open(f"{output_dir}/broader_than_violations_{timestamp}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Violation_ID", "Source", "Target", "Cycle"])
            for i, v in enumerate(violations, 1):
                writer.writerow([i, v["source"], v["target"], " -> ".join(v["cycle"])])

    with open(f"{output_dir}/duplicates_{timestamp}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "Count"])
        for (s, t), c in duplicates.items():
            if c > 1:
                writer.writerow([s, t, c])

    with open(f"{output_dir}/self_loops_{timestamp}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["CUI", "Relation"])
        for cui, rel in self_loops:
            writer.writerow([cui, rel])

    with open(f"{output_dir}/analysis_statistics_{timestamp}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        for key, value in stats.items():
            writer.writerow([key, value])


# Main CLI
def main():
    parser = argparse.ArgumentParser(description="UMLS Inconsistency Checker")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to MRREL.RRF")
    parser.add_argument("--type", "-t", choices=["parent-child", "broader-than", "both"], required=True)
    args = parser.parse_args()

    start_time = time.time()
    logger.info("Parsing input file...")
    pc_edges, bt_edges, dupes, loops, rel_types = parse_mrrel(args.input)

    stats = {
        "Total Parent-Child Relationships": len(pc_edges),
        "Total Broader-Than Relationships": len(bt_edges),
        "Total Unique Relationship Types": len(rel_types),
        "Total Self-Loops": len(loops),
        "Total Duplicates": sum(1 for c in dupes.values() if c > 1)
    }

    if args.type in ["parent-child", "both"]:
        logger.info("Analyzing parent-child relationships...")
        pc_graph = defaultdict(list)
        for s, t in pc_edges:
            pc_graph[s].append(t)
        pc_start = time.time()
        cycles = detect_cycles(pc_graph)
        stats["Parent-Child Cycle Count"] = len(cycles)
        stats["Parent-Child Detection Time (s)"] = round(time.time() - pc_start, 2)
        logger.info(f"Detected {len(cycles)} parent-child cycles")
    else:
        cycles = []

    if args.type in ["broader-than", "both"]:
        logger.info("Analyzing broader-than relationships...")
        bt_graph = nx.DiGraph()
        bt_graph.add_edges_from(bt_edges)
        bt_start = time.time()
        violations = detect_broader_violations(bt_graph)
        stats["Broader-Than Violation Count"] = len(violations)
        stats["Broader-Than Detection Time (s)"] = round(time.time() - bt_start, 2)
        logger.info(f"Detected {len(violations)} broader-than violations")
    else:
        violations = []

    stats["Total Runtime (s)"] = round(time.time() - start_time, 2)
    save_results(cycles, violations, dupes, loops, stats)
    logger.info("Analysis complete. Results saved.")


if __name__ == "__main__":
    main()
