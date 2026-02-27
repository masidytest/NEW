# next_system.py
import torch
import torch.nn as nn
import torch.nn.functional as F
import random

# ---------------- Tools ----------------

from typing import Callable, Dict, Any, List

class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register(self, name, func):
        self.tools[name] = func
    
    def call(self, name, *args, **kwargs):
        if name not in self.tools:
            return f"[tool '{name}' not found]"
        try:
            return self.tools[name](*args, **kwargs)
        except Exception as e:
            return f"[tool '{name}' error: {e}]"
    
    def get(self, name):
        return self.tools.get(name)

# ---------------- Capability Registry ----------------

class Capability:
    def __init__(self, name: str, func: Callable, tags: List[str],
                 input_schema: Dict[str, Any] = None,
                 output_schema: Dict[str, Any] = None,
                 description: str = ""):
        self.name = name
        self.func = func
        self.tags = tags or []
        self.input_schema = input_schema or {}
        self.output_schema = output_schema or {}
        self.description = description
    
    def __repr__(self):
        return f"<Capability {self.name} tags={self.tags}>"

class CapabilityRegistry:
    def __init__(self):
        self._capabilities: Dict[str, Capability] = {}
    
    def register(self, name: str, func: Callable, tags: List[str],
                 input_schema: Dict[str, Any] = None,
                 output_schema: Dict[str, Any] = None,
                 description: str = ""):
        cap = Capability(name, func, tags, input_schema, output_schema, description)
        self._capabilities[name] = cap
        return cap
    
    def get(self, name: str) -> Capability:
        return self._capabilities.get(name)
    
    def all(self) -> List[Capability]:
        return list(self._capabilities.values())
    
    def find_by_tags(self, required_tags: List[str]) -> List[Capability]:
        res = []
        for cap in self._capabilities.values():
            if all(t in cap.tags for t in required_tags):
                res.append(cap)
        return res

# ---------------- Capability Gap Analyzer ----------------

class CapabilityGapAnalyzer:
    def __init__(self):
        self.gaps = []  # each: {goal, tags, missing_tags, timestamp}
    
    def log_gap(self, goal: str, tags, missing_tags):
        self.gaps.append({
            "goal": goal,
            "tags": tags,
            "missing_tags": missing_tags,
            "timestamp": time.time()
        })
    
    def summarize_gaps(self):
        # group by missing_tags
        from collections import Counter
        counter = Counter(tuple(sorted(g["missing_tags"])) for g in self.gaps)
        summaries = []
        for missing, count in counter.items():
            summaries.append({
                "missing_tags": list(missing),
                "count": count
            })
        return sorted(summaries, key=lambda x: x["count"], reverse=True)
    
    def propose_plugin_specs(self):
        specs = []
        for summary in self.summarize_gaps():
            tags = summary["missing_tags"]
            specs.append({
                "name": f"plugin_for_{'_'.join(tags)}",
                "tags": tags,
                "description": f"Capability to handle tasks requiring tags {tags}",
                "suggested_inputs": ["TBD"],
                "suggested_outputs": ["TBD"],
                "count": summary["count"]
            })
        return specs

def add_basic_tools(registry: ToolRegistry):
    import math
    
    def calc(expr: str):
        return str(eval(expr, {"__builtins__": {}}, {"math": math}))
    
    def now():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    registry.register("calc", calc)
    registry.register("now", lambda: now())

# --------- Tools: AI Papers ---------

import textwrap

def tool_fetch_ai_papers(query: str = "artificial intelligence", max_results: int = 5):
    # Stub: in production, call arXiv / Semantic Scholar / etc.
    # Here we return synthetic paper data
    papers = []
    for i in range(max_results):
        papers.append({
            "title": f"Paper {i+1} about {query}",
            "abstract": f"This is a synthetic abstract for a paper about {query}. "
                        f"It discusses methods, experiments, and conclusions."
        })
    return papers

def tool_summarize_papers(papers):
    # Simple concatenation + truncation
    if isinstance(papers, str):
        return papers  # already a string
    summaries = []
    for p in papers:
        if isinstance(p, dict):
            summaries.append(f"- {p.get('title', 'Unknown')}: {p.get('abstract', 'No abstract')}")
        else:
            summaries.append(f"- {str(p)}")
    text = "\n".join(summaries)
    return textwrap.shorten(text, width=1000, placeholder=" ...")

# --------- Tools: Codebase Analysis ---------

import os

def tool_list_code_files(root_dir: str = ".", exts=(".py",)):
    files = []
    try:
        for base, _, names in os.walk(root_dir):
            for n in names:
                if n.endswith(exts):
                    files.append(os.path.join(base, n))
    except Exception as e:
        return f"[error listing files: {e}]"
    return files[:20]  # limit to first 20 files

def tool_read_file(path: str, max_bytes: int = 5000):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(max_bytes)
    except Exception as e:
        return f"[error reading {path}: {e}]"

def tool_analyze_code_snippet(snippet: str):
    # Stub: placeholder analysis
    lines = snippet.count('\n')
    return f"Code analysis (length={len(snippet)} chars, {lines} lines). " \
           f"Potential refactors: extract functions, improve naming, add documentation, " \
           f"consider design patterns."

def add_research_tools(registry: ToolRegistry):
    registry.register("fetch_ai_papers", tool_fetch_ai_papers)
    registry.register("summarize_papers", tool_summarize_papers)

def add_codebase_tools(registry: ToolRegistry):
    registry.register("list_code_files", tool_list_code_files)
    registry.register("read_file", tool_read_file)
    registry.register("analyze_code_snippet", tool_analyze_code_snippet)

# ---------------- Tokenizer (character-level) ----------------

class SimpleTokenizer:
    def __init__(self):
        chars = ["<pad>", "<bos>", "<eos>"] + [chr(i) for i in range(32, 127)]
        self.stoi = {c: i for i, c in enumerate(chars)}
        self.itos = {i: c for c, i in self.stoi.items()}
        self.pad_id = self.stoi["<pad>"]
        self.bos_id = self.stoi["<bos>"]
        self.eos_id = self.stoi["<eos>"]
    
    def encode(self, text, max_len=128):
        ids = [self.bos_id]
        for ch in text[: max_len - 2]:
            ids.append(self.stoi.get(ch, self.stoi["?"]))
        ids.append(self.eos_id)
        if len(ids) < max_len:
            ids += [self.pad_id] * (max_len - len(ids))
        return torch.tensor(ids, dtype=torch.long)
    
    def decode(self, ids):
        chars = []
        for i in ids:
            c = self.itos.get(int(i), "?")
            if c in ["<pad>", "<bos>", "<eos>"]:
                continue
            chars.append(c)
        return "".join(chars)

# ---------------- Upgraded Core Model ----------------

class CoreNet(nn.Module):
    def __init__(self, vocab_size, d_model=128, hidden=256, layers=2):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        self.rnn = nn.GRU(d_model, hidden, num_layers=layers, batch_first=True, bidirectional=True)
        self.attn = nn.MultiheadAttention(embed_dim=hidden * 2, num_heads=4, batch_first=True)
        self.out = nn.Linear(hidden * 2, vocab_size)   # for next-token prediction
        self.proj = nn.Linear(hidden * 2, d_model)     # for memory vectors
    
    def forward(self, input_ids):
        x = self.embed(input_ids)          # [B, T, D]
        h, _ = self.rnn(x)                 # [B, T, 2H] (bidirectional)
        attn_out, _ = self.attn(h, h, h)   # [B, T, 2H] (self-attention)
        logits = self.out(attn_out)        # [B, T, V]
        return logits
    
    def encode_text(self, input_ids):
        x = self.embed(input_ids.unsqueeze(0))  # [1, T, D]
        h, _ = self.rnn(x)                      # [1, T, 2H]
        attn_out, _ = self.attn(h, h, h)        # [1, T, 2H]
        vec = self.proj(attn_out[:, -1, :])     # [1, D]
        return vec.squeeze(0)                   # [D]

# ---------------- Structured Memory with Consolidation ----------------

import time

class MemoryItem:
    def __init__(self, vec, text, mtype, tags, importance, timestamp=None):
        self.vec = vec
        self.text = text
        self.mtype = mtype
        self.tags = tags or []
        self.base_importance = importance
        self.timestamp = timestamp or time.time()
    
    @property
    def age_days(self):
        return (time.time() - self.timestamp) / 86400.0
    
    @property
    def effective_importance(self):
        # simple decay: importance / (1 + age)
        return self.base_importance / (1.0 + self.age_days)

class MemoryStore:
    def __init__(self, dim):
        self.items = []
        self.dim = dim
    
    def add(self, vec, text, mtype="episode", tags=None, importance=1.0):
        item = MemoryItem(
            vec=vec.detach().cpu(),
            text=text,
            mtype=mtype,
            tags=tags or [],
            importance=importance,
            timestamp=time.time()
        )
        self.items.append(item)
        return item
    
    def _score(self, query_vec, item, query_tags):
        # vector similarity
        sim = F.cosine_similarity(
            query_vec.unsqueeze(0),
            item.vec.unsqueeze(0)
        ).item()
        
        # recency (scaled 0–1)
        age = time.time() - item.timestamp
        recency = 1 / (1 + age)
        
        # tag match
        tag_score = 0
        if query_tags:
            tag_score = len(set(query_tags) & set(item.tags)) / max(1, len(item.tags))
        
        # use effective importance (with decay)
        imp = item.effective_importance
        
        # weighted total score
        total = (0.55 * sim) + (0.20 * recency) + (0.15 * tag_score) + (0.10 * imp)
        return total
    
    def query(self, vec, top_k=5, query_tags=None):
        if not self.items:
            return []
        
        scores = []
        for item in self.items:
            s = self._score(vec, item, query_tags)
            scores.append((s, item))
        
        scores.sort(key=lambda x: x[0], reverse=True)
        results = []
        for s, item in scores[:top_k]:
            results.append({
                "score": s,
                "text": item.text,
                "type": item.mtype,
                "tags": item.tags,
                "importance": item.effective_importance
            })
        return results
    
    def consolidate(self, sim_threshold=0.9, min_effective_importance=0.05):
        """
        Consolidate memory: prune low-importance items and merge similar ones
        """
        # 1) prune low-importance, old items
        self.items = [
            m for m in self.items
            if m.effective_importance >= min_effective_importance
        ]
        
        # 2) merge very similar items
        merged = []
        used = set()
        
        for i, mi in enumerate(self.items):
            if i in used:
                continue
            group = [mi]
            for j, mj in enumerate(self.items[i+1:], start=i+1):
                if j in used:
                    continue
                sim = F.cosine_similarity(mi.vec, mj.vec, dim=0).item()
                if sim >= sim_threshold and set(mi.tags) == set(mj.tags):
                    group.append(mj)
                    used.add(j)
            
            if len(group) == 1:
                merged.append(mi)
            else:
                # summary text: simple concatenation
                summary_text = " | ".join(g.text for g in group)
                avg_vec = torch.stack([g.vec for g in group], dim=0).mean(dim=0)
                avg_importance = sum(g.base_importance for g in group) / len(group)
                newest_ts = max(g.timestamp for g in group)
                merged.append(MemoryItem(
                    avg_vec, summary_text, mi.mtype, mi.tags, avg_importance, newest_ts
                ))
        
        self.items = merged
        print(f"[memory] consolidated to {len(self.items)} items")

class HierarchicalMemory:
    def __init__(self, short_term: MemoryStore, mid_term: MemoryStore, long_term: MemoryStore):
        self.short_term = short_term
        self.mid_term = mid_term
        self.long_term = long_term
        self.items = []  # unified view for compatibility
    
    def add(self, vec, text, mtype="episode", tags=None, importance=1.0):
        # route by importance
        if importance >= 2.0:
            item = self.long_term.add(vec, text, mtype, tags, importance)
        elif importance >= 1.0:
            item = self.mid_term.add(vec, text, mtype, tags, importance)
        else:
            item = self.short_term.add(vec, text, mtype, tags, importance)
        
        # maintain unified view
        self.items = self.short_term.items + self.mid_term.items + self.long_term.items
        return item
    
    def query(self, vec, top_k=5, query_tags=None):
        hits = []
        hits += self.short_term.query(vec, top_k=top_k, query_tags=query_tags)
        hits += self.mid_term.query(vec, top_k=top_k, query_tags=query_tags)
        hits += self.long_term.query(vec, top_k=top_k, query_tags=query_tags)
        # sort by score
        hits = sorted(hits, key=lambda h: h.get("score", 0.0), reverse=True)
        return hits[:top_k]
    
    def consolidate(self):
        self.short_term.consolidate()
        self.mid_term.consolidate()
        self.long_term.consolidate()
        # update unified view
        self.items = self.short_term.items + self.mid_term.items + self.long_term.items

# ---------------- World state ----------------

class WorldState:
    def __init__(self):
        self.state = {}
    
    def set(self, key, value):
        self.state[key] = value
    
    def get(self, key, default=None):
        return self.state.get(key, default)
    
    def snapshot(self):
        return dict(self.state)

# ---------------- Long-Term Goals & Scheduler ----------------

from enum import Enum, auto

class GoalStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    PAUSED = auto()
    FAILED = auto()

class LongTermGoal:
    def __init__(self, description, priority=1.0, tags=None):
        self.id = f"goal-{int(time.time() * 1000)}"
        self.description = description
        self.priority = priority
        self.tags = tags or []
        self.status = GoalStatus.PENDING
        self.created_at = time.time()
        self.updated_at = self.created_at
        self.progress_notes = []
        self.last_run_ts = None
    
    def add_progress(self, note):
        self.progress_notes.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {note}")
        self.updated_at = time.time()
    
    @property
    def age_days(self):
        return (time.time() - self.created_at) / 86400.0
    
    @property
    def score(self):
        # priority boosted by recency of work and penalized by age
        recency_bonus = 0.0
        if self.last_run_ts is not None:
            recency_bonus = 1.0 / (1.0 + (time.time() - self.last_run_ts) / 3600.0)
        return self.priority + recency_bonus - 0.1 * self.age_days

class LongTermGoalManager:
    def __init__(self):
        self.goals = {}
    
    def add_goal(self, description, priority=1.0, tags=None):
        g = LongTermGoal(description, priority, tags)
        self.goals[g.id] = g
        return g.id
    
    def get_goal(self, goal_id):
        return self.goals.get(goal_id)
    
    def list_goals(self, status_filter=None):
        if status_filter is None:
            return list(self.goals.values())
        return [g for g in self.goals.values() if g.status == status_filter]
    
    def pick_next_goal(self):
        candidates = [g for g in self.goals.values()
                      if g.status in (GoalStatus.PENDING, GoalStatus.IN_PROGRESS)]
        if not candidates:
            return None
        # pick by highest score
        best = max(candidates, key=lambda g: g.score)
        best.status = GoalStatus.IN_PROGRESS
        best.last_run_ts = time.time()
        return best
    
    def mark_done(self, goal_id, note=None):
        g = self.goals.get(goal_id)
        if not g:
            return
        g.status = GoalStatus.DONE
        if note:
            g.add_progress(f"Completed: {note}")
    
    def add_progress(self, goal_id, note):
        g = self.goals.get(goal_id)
        if not g:
            return
        g.add_progress(note)

# ---------------- Expressive Planner with Replanning ----------------

from collections import Counter

class PlanPatternLogger:
    def __init__(self):
        self.records = []  # each: {goal, tags, steps, success}
    
    def log(self, goal, tags, plan, success: bool):
        pattern = {
            "goal": goal,
            "tags": tags or [],
            "steps": [s["type"] for s in plan],
            "success": success,
        }
        self.records.append(pattern)
    
    def get_successful_patterns(self, tag=None, min_success=1):
        patterns = [r for r in self.records if r["success"]]
        if tag:
            patterns = [r for r in patterns if tag in r["tags"]]
        # group by step sequence
        seqs = Counter(tuple(p["steps"]) for p in patterns)
        return [list(seq) for seq, count in seqs.items() if count >= min_success]

class CapabilityAwarePlanner:
    def __init__(self, agent):
        self.agent = agent
    
    def infer_tags(self, goal: str):
        g = goal.lower()
        tags = []
        
        if any(w in g for w in ["time", "date", "now"]):
            tags.append("time")
        if any(w in g for w in ["sum", "add", "multiply", "divide", "calc"]):
            tags.append("math")
        if any(w in g for w in ["paper", "research", "ai papers", "arxiv"]):
            tags.extend(["research", "papers"])
        if any(w in g for w in ["code", "repo", "refactor", "bug", "debug"]):
            tags.append("code")
        if any(w in g for w in ["csv", "json", "data", "dataset"]):
            tags.append("data")
        if any(w in g for w in ["image", "picture", "generate image"]):
            tags.append("image")
        if any(w in g for w in ["speech", "audio", "voice"]):
            tags.append("speech")
        
        return tags
    
    def choose_capabilities(self, tags):
        caps = []
        for tag in tags:
            matches = self.agent.capabilities.find_by_tags([tag])
            caps.extend(matches)
        # deduplicate
        unique = {}
        for c in caps:
            unique[c.name] = c
        return list(unique.values())
    
    def make_plan(self, goal: str, memory_hits=None):
        tags = self.infer_tags(goal)
        caps = self.choose_capabilities(tags)
        
        # Log capability gaps
        available_tags = set()
        for cap in self.agent.capabilities.all():
            available_tags.update(cap.tags)
        
        missing = [t for t in tags if t not in available_tags]
        if missing:
            self.agent.capability_gaps.log_gap(goal, tags, missing)
        
        steps = []
        step_id = 1
        
        steps.append({
            "step": step_id,
            "type": "think",
            "description": f"Understand the goal: '{goal}' and relevant tags {tags}"
        })
        step_id += 1
        
        if memory_hits:
            steps.append({
                "step": step_id,
                "type": "recall",
                "description": "Review relevant memories"
            })
            step_id += 1
        
        # add capability-based actions
        for cap in caps:
            steps.append({
                "step": step_id,
                "type": "act",
                "tool": cap.name,
                "description": f"Use capability '{cap.name}' ({cap.description})"
            })
            step_id += 1
        
        steps.append({
            "step": step_id,
            "type": "reason",
            "description": "Integrate all results and derive insights"
        })
        step_id += 1
        
        steps.append({
            "step": step_id,
            "type": "answer",
            "description": "Produce final response"
        })
        
        return steps
    
    def replan_if_needed(self, goal, plan, tool_results, critique_text):
        """
        Simple heuristic for replanning
        """
        needs_more_reasoning = any(
            w in critique_text.lower() for w in ["missing", "incomplete", "unclear"]
        )
        
        new_plan = []
        for step in plan:
            if step["type"] == "reason" and any(
                "already answered" in str(v).lower() for v in tool_results.values()
            ):
                continue
            new_plan.append(step)
        
        if needs_more_reasoning:
            last_step_num = new_plan[-1]["step"]
            new_plan.insert(-1, {
                "step": last_step_num,
                "type": "reason",
                "description": "Additional reasoning to address critique"
            })
            for idx, s in enumerate(new_plan, start=1):
                s["step"] = idx
        
        return new_plan

class MetaPlanner:
    def __init__(self, base_planner, pattern_logger: PlanPatternLogger):
        self.base_planner = base_planner
        self.pattern_logger = pattern_logger
    
    def infer_tags(self, goal: str):
        return self.base_planner.infer_tags(goal)
    
    def make_plan(self, goal: str, memory_hits=None):
        tags = self.infer_tags(goal)
        # try to reuse a successful pattern
        for tag in tags:
            patterns = self.pattern_logger.get_successful_patterns(tag=tag, min_success=2)
            if patterns:
                steps_seq = patterns[0]  # pick first for now
                # rebuild a plan with same step types but fresh descriptions
                base_plan = self.base_planner.make_plan(goal, memory_hits)
                by_type = {s["type"]: s for s in base_plan}
                plan = []
                step_id = 1
                for t in steps_seq:
                    template = by_type.get(t)
                    if not template:
                        continue
                    step_dict = {
                        "step": step_id,
                        "type": t,
                        "description": template["description"]
                    }
                    if "tool" in template:
                        step_dict["tool"] = template["tool"]
                    plan.append(step_dict)
                    step_id += 1
                if plan:
                    return plan
        # fallback: normal planner
        return self.base_planner.make_plan(goal, memory_hits)
    
    def replan_if_needed(self, goal, plan, tool_results, critique_text):
        return self.base_planner.replan_if_needed(goal, plan, tool_results, critique_text)

# ---------------- Reasoning Engine ----------------

class ReasoningEngine:
    def __init__(self, core, tokenizer, device, tools):
        self.core = core
        self.tokenizer = tokenizer
        self.device = device
        self.tools = tools
    
    def run(self, plan, memory_hits, goal):
        reasoning_context = []
        tool_results = {}
        
        for step in plan:
            stype = step["type"]
            desc = step["description"]
            
            if stype == "think":
                reasoning_context.append(f"Goal analysis: {goal}")
            
            elif stype == "recall":
                if memory_hits:
                    for hit in memory_hits:
                        reasoning_context.append(f"Relevant memory: {hit['text']}")
            
            elif stype == "reason":
                reasoning_context.append(f"Sub-goal reasoning: {desc}")
            
            elif stype == "act":
                tool_name = step.get("tool")
                if tool_name == "calc":
                    result = self.tools.call("calc", goal)
                elif tool_name == "now":
                    result = self.tools.call("now")
                elif tool_name == "fetch_ai_papers":
                    result = self.tools.call("fetch_ai_papers", query="artificial intelligence", max_results=5)
                elif tool_name == "summarize_papers":
                    # Get papers from previous tool result if available
                    papers = tool_results.get("fetch_ai_papers", [])
                    result = self.tools.call("summarize_papers", papers)
                elif tool_name == "list_code_files":
                    result = self.tools.call("list_code_files", root_dir=".", exts=(".py",))
                elif tool_name == "read_file":
                    # Get first file from previous list_code_files result
                    files = tool_results.get("list_code_files", [])
                    if files and isinstance(files, list) and len(files) > 0:
                        result = self.tools.call("read_file", files[0], max_bytes=5000)
                    else:
                        result = "[no files to read]"
                elif tool_name == "analyze_code_snippet":
                    # Get code from previous read_file result
                    code = tool_results.get("read_file", "")
                    result = self.tools.call("analyze_code_snippet", code)
                else:
                    result = self.tools.call(tool_name)
                tool_results[tool_name] = result
                reasoning_context.append(f"Tool '{tool_name}' result: {result}")
            
            elif stype == "answer":
                final_prompt = "Reasoning:\n" + "\n".join(reasoning_context) + "\n\nAnswer:"
                answer = self._generate(final_prompt)
                return answer, "\n".join(reasoning_context)
        
        return "I could not complete the reasoning process.", ""
    
    def _generate(self, prompt):
        self.core.eval()
        ids = self.tokenizer.encode(prompt).to(self.device).unsqueeze(0)
        with torch.no_grad():
            for _ in range(100):
                logits = self.core(ids)
                next_logits = logits[0, -1, :]
                probs = F.softmax(next_logits, dim=-1)
                next_id = torch.multinomial(probs, num_samples=1)
                ids = torch.cat([ids, next_id.unsqueeze(0)], dim=1)
                if next_id.item() == self.tokenizer.eos_id:
                    break
        return self.tokenizer.decode(ids[0])

# ---------------- Stable Continuous Learning ----------------

class ContinuousLearner:
    def __init__(self, agent, lr=5e-5, replay_size=64):
        self.agent = agent
        self.core = agent.core
        self.tokenizer = agent.tokenizer
        
        self.optimizer = torch.optim.Adam(self.core.parameters(), lr=lr)
        self.scheduler = torch.optim.lr_scheduler.ExponentialLR(self.optimizer, gamma=0.999)
        self.loss_fn = nn.CrossEntropyLoss(ignore_index=self.tokenizer.pad_id)
        
        self.replay_buffer = []  # list of MemoryItem
        self.replay_size = replay_size
    
    def add_to_replay(self, mem_item):
        self.replay_buffer.append(mem_item)
        if len(self.replay_buffer) > self.replay_size:
            self.replay_buffer.pop(0)
    
    def _sample_from_replay(self, k):
        if not self.replay_buffer:
            return []
        k = min(k, len(self.replay_buffer))
        idxs = random.sample(range(len(self.replay_buffer)), k)
        return [self.replay_buffer[i] for i in idxs]
    
    def sample_memories(self, batch_size=4):
        # importance * recency
        items = sorted(
            self.agent.memory.items,
            key=lambda m: m.effective_importance,
            reverse=True
        )
        main = items[:batch_size]
        replay = self._sample_from_replay(batch_size // 2)
        return main + replay
    
    def train_step(self, batch_size=4, max_len=128):
        batch = self.sample_memories(batch_size)
        if not batch:
            return None
        
        total_loss = 0.0
        
        for item in batch:
            text = item.text
            ids = self.tokenizer.encode(text, max_len=max_len).to(self.agent.device)
            if ids.size(0) < 2:
                continue
            inp = ids[:-1].unsqueeze(0)
            tgt = ids[1:].unsqueeze(0)
            
            logits = self.core(inp)
            loss = self.loss_fn(logits.view(-1, logits.size(-1)), tgt.view(-1))
            
            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.core.parameters(), max_norm=1.0)
            self.optimizer.step()
            
            total_loss += loss.item()
        
        self.scheduler.step()
        return total_loss / max(1, len(batch))

# ---------------- Self-Evaluation ----------------

class SelfEvaluator:
    def __init__(self, core, tokenizer, device):
        self.core = core
        self.tokenizer = tokenizer
        self.device = device
    
    def evaluate(self, goal, reasoning_context, draft_answer):
        critique_prompt = (
            "Evaluate the following answer.\n\n"
            f"Goal: {goal}\n"
            f"Reasoning:\n{reasoning_context}\n\n"
            f"Draft answer: {draft_answer}\n\n"
            "Critique the answer briefly and suggest improvements:"
        )
        
        critique = self._generate(critique_prompt)
        
        refine_prompt = (
            "Improve the answer based on this critique.\n\n"
            f"Goal: {goal}\n"
            f"Reasoning:\n{reasoning_context}\n"
            f"Draft answer: {draft_answer}\n"
            f"Critique: {critique}\n\n"
            "Improved answer:"
        )
        
        improved = self._generate(refine_prompt)
        return improved
    
    def _generate(self, prompt):
        self.core.eval()
        ids = self.tokenizer.encode(prompt).to(self.device).unsqueeze(0)
        with torch.no_grad():
            for _ in range(100):
                logits = self.core(ids)
                next_logits = logits[0, -1, :]
                probs = F.softmax(next_logits, dim=-1)
                next_id = torch.multinomial(probs, num_samples=1)
                ids = torch.cat([ids, next_id.unsqueeze(0)], dim=1)
                if next_id.item() == self.tokenizer.eos_id:
                    break
        return self.tokenizer.decode(ids[0])

# ---------------- Unified Cognitive Engine ----------------

class CognitiveEngine:
    def __init__(self, agent, passes=3, consolidate_every=20):
        self.agent = agent
        self.passes = passes
        self.consolidate_every = consolidate_every
        self._call_count = 0
    
    def run(self, goal):
        """
        Unified cognitive loop with multi-pass reasoning,
        replanning, and periodic memory consolidation.
        """
        state = {
            "goal": goal,
            "vec": None,
            "mem_hits": None,
            "plan": None,
            "answer": None,
            "learning_loss": None
        }
        
        # Stage 1: Encode the goal
        state["vec"] = self.agent.encode(goal)
        
        # Stage 2: Query memory with shared state
        state["mem_hits"] = self.agent.memory.query(
            state["vec"], 
            top_k=5, 
            query_tags=["goal", "conversation"]
        )
        
        # Stage 3: Plan using memory context
        state["plan"] = self.agent.planner.make_plan(
            goal, 
            memory_hits=state["mem_hits"]
        )
        
        # Stage 4: Multi-pass reasoning loop with replanning
        draft = None
        context = None
        critique_text = ""
        tool_results = {}
        
        for pass_num in range(self.passes):
            # Execute reasoning with full context
            draft, context = self.agent.reasoner.run(
                state["plan"], 
                state["mem_hits"], 
                goal
            )
            
            # Self-evaluate and refine
            draft = self.agent.evaluator.evaluate(goal, context, draft)
            
            # Optional: replan after first pass
            if pass_num == 0:
                state["plan"] = self.agent.planner.replan_if_needed(
                    goal, state["plan"], tool_results, critique_text
                )
        
        state["answer"] = draft
        
        # Stage 5: Update memory with refined answer and add to replay
        mem_item = self.agent.memory.add(
            state["vec"],
            f"Goal: {goal} | Answer: {state['answer']}",
            mtype="episode",
            tags=["conversation", "goal"],
            importance=1.0
        )
        self.agent.learner.add_to_replay(mem_item)
        
        # Stage 6: Update world state
        self.agent.world.set("last_goal", goal)
        self.agent.world.set("last_plan", state["plan"])
        self.agent.world.set("last_answer", state["answer"])
        self.agent.world.set("last_state", state)
        
        # Stage 7: Continuous learning from experience
        state["learning_loss"] = self.agent.learner.train_step(batch_size=3)
        if state["learning_loss"] is not None:
            print(f"[learning] loss={state['learning_loss']:.4f}")
        
        # Stage 8: Periodic memory consolidation
        self._call_count += 1
        if self._call_count % self.consolidate_every == 0:
            self.agent.memory.consolidate()
        
        # Stage 9: Log plan pattern for meta-learning
        success = True  # heuristic: assume success (can refine later based on evaluation)
        self.agent.plan_logger.log(goal, self.agent.planner.infer_tags(goal), state["plan"], success)
        
        return state["answer"]
    
    def run_autonomous_cycle(self):
        """
        One autonomous tick:
        - pick a long-term goal
        - run the cognitive loop on it
        - store progress
        """
        goal = self.agent.long_term_goals.pick_next_goal()
        if goal is None:
            return None, "No active long-term goals."
        
        answer = self.run(goal.description)
        
        # record progress
        goal.add_progress(f"Ran cognitive loop. Latest answer: {answer[:200]}")
        # you can decide when to mark done; for now, keep IN_PROGRESS
        return goal, answer

# ---------------- Agent (ties everything together) ----------------

class Agent:
    def __init__(self, device="cpu", reasoning_passes=3):
        self.device = device
        self.tokenizer = SimpleTokenizer()
        vocab_size = len(self.tokenizer.stoi)
        self.core = CoreNet(vocab_size=vocab_size).to(self.device)
        
        # Hierarchical memory
        self.short_mem = MemoryStore(dim=128)
        self.mid_mem = MemoryStore(dim=128)
        self.long_mem = MemoryStore(dim=128)
        self.memory = HierarchicalMemory(self.short_mem, self.mid_mem, self.long_mem)
        
        self.world = WorldState()
        
        # Tools (legacy)
        self.tools = ToolRegistry()
        add_basic_tools(self.tools)
        add_research_tools(self.tools)
        add_codebase_tools(self.tools)
        
        # Capability system
        self.capabilities = CapabilityRegistry()
        self.capability_gaps = CapabilityGapAnalyzer()
        self._register_core_capabilities()
        
        # Load plugins
        self._load_plugins()
        
        # Meta-planner with capability awareness
        self.plan_logger = PlanPatternLogger()
        self.capability_planner = CapabilityAwarePlanner(self)
        self.planner = MetaPlanner(self.capability_planner, self.plan_logger)
        
        self.reasoner = ReasoningEngine(self.core, self.tokenizer, self.device, self.tools)
        self.learner = ContinuousLearner(self)
        self.evaluator = SelfEvaluator(self.core, self.tokenizer, self.device)
        self.long_term_goals = LongTermGoalManager()
        self.engine = CognitiveEngine(self, passes=reasoning_passes)
    
    def _register_core_capabilities(self):
        """Register all tools as capabilities with tags and schemas"""
        # Math
        self.capabilities.register(
            name="calc",
            func=self.tools.get("calc"),
            tags=["math", "utility"],
            input_schema={"expression": "str"},
            output_schema={"result": "float"},
            description="Basic calculator for arithmetic operations"
        )
        
        # Time
        self.capabilities.register(
            name="now",
            func=self.tools.get("now"),
            tags=["time", "utility"],
            output_schema={"timestamp": "str"},
            description="Get current date and time"
        )
        
        # Research
        self.capabilities.register(
            name="fetch_ai_papers",
            func=self.tools.get("fetch_ai_papers"),
            tags=["web", "research", "papers"],
            input_schema={"query": "str", "max_results": "int"},
            output_schema={"papers": "list"},
            description="Fetch AI research papers from various sources"
        )
        
        self.capabilities.register(
            name="summarize_papers",
            func=self.tools.get("summarize_papers"),
            tags=["nlp", "summarization", "research"],
            input_schema={"papers": "list"},
            output_schema={"summary": "str"},
            description="Summarize research papers into concise text"
        )
        
        # Code analysis
        self.capabilities.register(
            name="list_code_files",
            func=self.tools.get("list_code_files"),
            tags=["code", "files", "repo"],
            input_schema={"root_dir": "str"},
            output_schema={"files": "list"},
            description="List all code files in a directory"
        )
        
        self.capabilities.register(
            name="read_file",
            func=self.tools.get("read_file"),
            tags=["code", "files"],
            input_schema={"path": "str", "max_bytes": "int"},
            output_schema={"content": "str"},
            description="Read contents of a file"
        )
        
        self.capabilities.register(
            name="analyze_code_snippet",
            func=self.tools.get("analyze_code_snippet"),
            tags=["code", "analysis"],
            input_schema={"snippet": "str"},
            output_schema={"analysis": "str"},
            description="Analyze code and suggest improvements"
        )
    
    def _load_plugins(self):
        """Load plugins from plugins folder"""
        try:
            from plugin_loader import load_plugins
            load_plugins(self.capabilities)
        except Exception as e:
            print(f"[Agent] Plugin loading error: {e}")
    
    def encode(self, text: str):
        ids = self.tokenizer.encode(text).to(self.device)
        vec = self.core.encode_text(ids)
        return vec
    
    def generate_next(self, prompt: str, max_len=100):
        self.core.eval()
        ids = self.tokenizer.encode(prompt).to(self.device).unsqueeze(0)
        with torch.no_grad():
            for _ in range(max_len):
                logits = self.core(ids)
                next_logits = logits[0, -1, :]
                probs = F.softmax(next_logits, dim=-1)
                next_id = torch.multinomial(probs, num_samples=1)
                ids = torch.cat([ids, next_id.unsqueeze(0)], dim=1)
                if next_id.item() == self.tokenizer.eos_id:
                    break
        return self.tokenizer.decode(ids[0])
    
    def handle(self, user_input: str) -> str:
        """
        Main entry point - delegates to unified cognitive engine
        """
        return self.engine.run(user_input)
    
    def add_long_term_goal(self, description, priority=1.0, tags=None):
        """Add a long-term goal to the autonomous system"""
        return self.long_term_goals.add_goal(description, priority, tags)
    
    def list_long_term_goals(self):
        """List all long-term goals"""
        return self.long_term_goals.list_goals()
    
    def run_autonomous_cycle(self):
        """Run one autonomous cycle on long-term goals"""
        return self.engine.run_autonomous_cycle()
    
    def get_capability_gaps(self):
        """Get summary of missing capabilities"""
        return self.capability_gaps.summarize_gaps()
    
    def propose_new_plugins(self):
        """Get plugin specifications for missing capabilities"""
        return self.capability_gaps.propose_plugin_specs()

# ---------------- Training loop ----------------

def train_core_on_text(agent: Agent, texts, epochs=5, max_len=128, lr=1e-3):
    device = agent.device
    tok = agent.tokenizer
    model = agent.core
    model.train()
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss(ignore_index=tok.pad_id)
    
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        random.shuffle(texts)
        for text in texts:
            ids = tok.encode(text, max_len=max_len).to(device)
            inp = ids[:-1].unsqueeze(0)   # input
            tgt = ids[1:].unsqueeze(0)   # target
            logits = model(inp)          # [1, T, V]
            loss = loss_fn(logits.view(-1, logits.size(-1)), tgt.view(-1))
            opt.zero_grad()
            loss.backward()
            opt.step()
            total_loss += loss.item()
        avg = total_loss / max(1, len(texts))
        print(f"Epoch {epoch}: loss={avg:.4f}")

# ---------------- Main ----------------

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    agent = Agent(device=device)
    
    # small demo training data (replace with your own later)
    demo_texts = [
        "hello, this is a new brain.",
        "this system has memory and planning.",
        "the goal is to become more advanced over time.",
        "it can remember previous goals and answers.",
    ]
    print("Training core network on small demo texts...")
    train_core_on_text(agent, demo_texts, epochs=10, max_len=80, lr=1e-3)
    
    print("\nSystem ready. Type 'exit' to quit.\n")
    print("Commands:")
    print("  - Type a message for interactive mode")
    print("  - Type 'add goal: <description>' to add a long-term goal")
    print("  - Type 'list goals' to see all long-term goals")
    print("  - Type 'auto' to run one autonomous cycle")
    print("  - Type 'demo research' to add AI research goal")
    print("  - Type 'demo codebase' to add codebase analysis goal")
    print("  - Type 'gaps' to see capability gaps")
    print("  - Type 'plugins' to see proposed new plugins")
    print("  - Type 'capabilities' to list all capabilities")
    print("  - Type 'exit' to quit\n")
    
    while True:
        user = input("You: ").strip()
        if user.lower() in ["exit", "quit"]:
            break
        elif user.lower().startswith("add goal:"):
            goal_desc = user[9:].strip()
            goal_id = agent.add_long_term_goal(goal_desc, priority=1.0, tags=["user-defined"])
            print(f"Agent: Added long-term goal [{goal_id}]: {goal_desc}\n")
        elif user.lower() == "list goals":
            goals = agent.list_long_term_goals()
            if not goals:
                print("Agent: No long-term goals yet.\n")
            else:
                print("Agent: Long-term goals:")
                for g in goals:
                    print(f"  [{g.id}] {g.status.name}: {g.description} (priority={g.priority:.2f}, score={g.score:.2f})")
                print()
        elif user.lower() == "demo research":
            goal_id = agent.add_long_term_goal(
                "Continuously read new AI papers and maintain an evolving summary and idea map",
                priority=3.0,
                tags=["research", "ai-papers"]
            )
            print(f"Agent: Added AI research goal [{goal_id}]\n")
        elif user.lower() == "demo codebase":
            goal_id = agent.add_long_term_goal(
                "Continuously analyze my codebase and suggest refactors and architecture improvements",
                priority=2.5,
                tags=["codebase", "refactor"]
            )
            print(f"Agent: Added codebase analysis goal [{goal_id}]\n")
        elif user.lower() == "auto":
            print("Agent: Running autonomous cycle...")
            goal, answer = agent.run_autonomous_cycle()
            if goal is None:
                print(f"Agent: {answer}\n")
            else:
                print(f"Agent: [{goal.id}] {goal.description}")
                print(f"Answer: {answer}\n")
        elif user.lower() == "gaps":
            gaps = agent.get_capability_gaps()
            if not gaps:
                print("Agent: No capability gaps detected yet.\n")
            else:
                print("Agent: Capability gaps detected:")
                for gap in gaps:
                    print(f"  Missing tags: {gap['missing_tags']} (requested {gap['count']} times)")
                print()
        elif user.lower() == "plugins":
            specs = agent.propose_new_plugins()
            if not specs:
                print("Agent: No plugin proposals yet.\n")
            else:
                print("Agent: Proposed new plugins:")
                for spec in specs:
                    print(f"  {spec['name']}")
                    print(f"    Tags: {spec['tags']}")
                    print(f"    Description: {spec['description']}")
                    print(f"    Requested: {spec['count']} times")
                print()
        elif user.lower() == "capabilities":
            caps = agent.capabilities.all()
            print(f"Agent: {len(caps)} capabilities registered:")
            for cap in caps:
                print(f"  {cap.name}: {cap.description}")
                print(f"    Tags: {cap.tags}")
            print()
        else:
            answer = agent.handle(user)
            print("Agent:\n" + answer + "\n")

if __name__ == "__main__":
    main()
