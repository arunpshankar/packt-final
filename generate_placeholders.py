#!/usr/bin/env python3
"""
Generate placeholder images for every book figure.
Each image is a pastel-toned sketch-aesthetic panel containing:
  - Chapter + figure label
  - Figure title
  - Crisp AI image-generation prompt (copyable)
Saves to chapters/images/
"""
import os, textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

OUT = '/Users/arunprasathshankar/Desktop/repos/packt-final/chapters/images'
os.makedirs(OUT, exist_ok=True)

# Part accent colours (header bar)
PART_COLORS = {
    1: '#7FB069',   # sage green
    2: '#5B8DB8',   # dusty blue
    3: '#D4845A',   # warm coral
    4: '#9B7BB5',   # soft lavender
}

FIGURES = [
    # (filename, part, ch, fig_n, title, prompt)

    # ── Chapter 1 ──────────────────────────────────────────────
    ('ch01_fig01_probability_space.png', 1, 1, 1,
     'Probability as Area',
     'Flat technical illustration of a probability sample space: a large soft-grey rectangle '
     'labelled Omega representing the universal event, with two overlapping pastel ellipses '
     'inside labelled A and B, shaded in translucent sage-green and dusty-blue respectively, '
     'their intersection highlighted in soft teal. Clean sans-serif labels. Crisp black '
     'outlines. White background. Minimalist infographic style. Pastel color palette. '
     'No photorealism. 2D flat diagram.'),

    ('ch01_fig02_gradient_descent.png', 1, 1, 2,
     'Gradient Descent Loss Landscape',
     'Minimalist 2D line-art illustration of a gradient descent loss curve: smooth convex '
     'bowl-shaped curve in dusty blue on a white background, a red dot labelled "current '
     'parameters" on the slope, a green dot at the minimum labelled "optimal parameters", '
     'a dashed arrow curving downward from red to green labelled "gradient step". '
     'Clean axis labels Loss and Parameters. Pastel palette. Sketch aesthetic. '
     'No 3D perspective, purely flat 2D.'),

    # ── Chapter 2 ──────────────────────────────────────────────
    ('ch02_fig01_alignment_gap.png', 1, 2, 1,
     'The Alignment Gap',
     'Flat infographic showing two vertical columns side by side: left column labelled '
     '"Pre-trained LLM" with a brain icon and bullet traits (predicts tokens, no values, '
     'may be harmful); right column labelled "Aligned LLM" with a shield-plus-brain icon '
     'and traits (helpful, harmless, honest). A wide bridging arrow between columns labelled '
     '"RLHF / DPO / GRPO". Pastel sage green for left, dusty blue for right. Clean crisp '
     'arrows. White background. Modern flat design. Sans-serif typography. No photorealism.'),

    # ── Chapter 3 ──────────────────────────────────────────────
    ('ch03_fig01_agent_env_loop.png', 1, 3, 1,
     'Agent-Environment Interaction Loop',
     'Clean circular flow diagram: two rounded rectangles labelled "Agent" (dusty blue) '
     'and "Environment" (sage green), connected by two curved arrows. Top arrow from Agent '
     'to Environment labelled "Action a_t". Bottom arrow from Environment to Agent labelled '
     '"State s_{t+1}, Reward r_t". Small clock icon at bottom labelled "t -> t+1". '
     'White background. Crisp thin outlines. Flat minimalist style. Pastel palette. '
     'Technical diagram aesthetic.'),

    ('ch03_fig02_policy_types.png', 1, 3, 2,
     'Deterministic vs Stochastic Policy',
     'Side-by-side comparison diagram. Left panel labelled "Deterministic Policy": a state '
     'box with a single bold arrow pointing to one action box. Right panel labelled '
     '"Stochastic Policy": a state box with three arrows of different thicknesses pointing '
     'to three action boxes, each arrow annotated with a probability (0.6, 0.3, 0.1). '
     'Soft coral accent for deterministic, dusty blue for stochastic. Clean labels. '
     'White background. Flat technical illustration. Minimalist.'),

    # ── Chapter 5 ──────────────────────────────────────────────
    ('ch05_fig01_sft_pipeline.png', 2, 5, 1,
     'Supervised Fine-Tuning Pipeline',
     'Horizontal left-to-right flow diagram with five stages connected by right-pointing '
     'arrows: (1) "Curated Dataset" box with stacked document icon in warm coral; '
     '(2) "Tokeniser" box; (3) "Base LLM" large rounded rectangle in dusty blue with '
     'layer stack icon; (4) "Cross-Entropy Loss" box with formula symbol; '
     '(5) "Fine-tuned Model" box with checkmark in sage green. '
     'Thin crisp arrows. White background. Flat pastel infographic. Clean sans-serif labels.'),

    ('ch05_fig02_cold_start.png', 2, 5, 2,
     'The Cold-Start Problem',
     'Minimalist diagram showing a vertical axis labelled "Response Quality" and a '
     'horizontal axis labelled "Training Steps". Two curves: a dashed grey curve starting '
     'near zero labelled "RL from scratch (cold)" which rises slowly; a solid dusty-blue '
     'curve starting higher labelled "SFT warm start then RL" which rises faster and higher. '
     'A vertical dashed line labelled "Switch to RL" separates regions. Shaded gap between '
     'curves in soft coral. Legend. White background. Clean sketch style.'),

    # ── Chapter 6 ──────────────────────────────────────────────
    ('ch06_fig01_rlhf_pipeline.png', 2, 6, 1,
     'RLHF Three-Step Pipeline',
     'Vertical top-to-bottom flow diagram with three large numbered steps connected by '
     'downward arrows. Step 1 "SFT" box (sage green): base model plus human demonstrations '
     'arrow into fine-tuned model. Step 2 "Reward Model Training" box (dusty blue): pairs '
     'of responses with human preference labels arrow into reward model with scalar output. '
     'Step 3 "PPO RL" box (warm coral): policy updated by reward signal with KL penalty '
     'annotation. Crisp flat icons. White background. Pastel infographic.'),

    ('ch06_fig02_ppo_clipping.png', 2, 6, 2,
     'PPO Clipping Mechanism',
     'Mathematical diagram showing the PPO objective clipping function. Horizontal axis '
     'labelled "probability ratio r" from 0 to 2.5. Vertical axis labelled "clipped '
     'objective". A solid dusty-blue line showing the unclipped ratio times advantage. '
     'A dashed coral line showing the clip(r, 1-eps, 1+eps) bounds. Shaded region between '
     '(1-eps) and (1+eps) in soft green labelled "allowed update zone". Clean annotations. '
     'White background. Technical sketch aesthetic.'),

    # ── Chapter 7 ──────────────────────────────────────────────
    ('ch07_fig01_dpo_vs_rlhf.png', 2, 7, 1,
     'DPO vs RLHF Comparison',
     'Two-column comparison diagram. Left column labelled "RLHF" (3 boxes stacked): '
     'SFT -> Reward Model -> PPO Loop, with curly brace annotation "3 separate models, '
     'complex pipeline". Right column labelled "DPO" (1 box): Policy trained directly on '
     'preference pairs, annotation "1 model, direct training". A bold "vs" separator '
     'between columns. Colour: RLHF in muted coral, DPO in sage green. Flat minimal '
     'infographic. White background. Clean arrows and labels.'),

    # ── Chapter 8 ──────────────────────────────────────────────
    ('ch08_fig01_online_dpo_loop.png', 2, 8, 1,
     'Online DPO Iterative Loop',
     'Circular flow diagram with four nodes: (1) "Current Policy" circle in dusty blue; '
     '(2) "Generate Response Pairs" box; (3) "Score with Reward Model" box; '
     '(4) "DPO Update" box in sage green. Clockwise curved arrows connecting all four. '
     'A small label on the loop "Repeat every N steps". White background. Crisp clean '
     'outline style. Flat pastel colours. Technical infographic.'),

    # ── Chapter 9 ──────────────────────────────────────────────
    ('ch09_fig01_reward_model_arch.png', 2, 9, 1,
     'Reward Model Architecture',
     'Vertical architecture diagram: at bottom a "Prompt + Response" input box, arrow up '
     'into a "Transformer Backbone" tall rectangle with horizontal layer lines in dusty '
     'blue, arrow up into a "Linear Head" small rectangle, arrow up into a single circle '
     'labelled "r (scalar reward)" in warm coral. Annotations: "Frozen or fine-tuned" '
     'beside backbone, "1 output neuron" beside head. White background. Clean flat '
     'technical diagram. Pastel palette.'),

    ('ch09_fig02_preference_annotation.png', 2, 9, 2,
     'Human Preference Annotation Pipeline',
     'Horizontal flow: "Prompt" box -> "LLM" circle -> two branching arrows labelled '
     '"Response A" and "Response B" going into a "Human Annotator" icon (person silhouette '
     'in dusty blue) -> a "Preference Label" diamond (A > B or B > A) -> '
     '"Preference Dataset" stacked-pages icon in sage green. Clean flat icons. '
     'Pastel colours. White background. Minimalist infographic.'),

    # ── Chapter 10 ──────────────────────────────────────────────
    ('ch10_fig01_grpo_sampling.png', 2, 10, 1,
     'GRPO Group Sampling',
     'Diagram showing one prompt box at left, with G=4 arrows fanning out to four response '
     'boxes labelled y1 through y4. Below each response box a small reward value badge '
     '(e.g. +1.2, -0.3, +0.8, +0.5). A horizontal baseline bar labelled "group mean '
     'reward" across all four. Vertical advantage arrows above/below baseline for each '
     'response. Dusty blue for responses, coral for below-baseline advantages, sage green '
     'for above-baseline. White background. Clean flat diagram.'),

    ('ch10_fig02_algo_comparison.png', 2, 10, 2,
     'GRPO vs RLOO vs KTO Algorithm Comparison',
     'Three-column comparison table rendered as a clean infographic. Columns: GRPO, RLOO, '
     'KTO. Rows: Baseline type, Needs reward model, Critic required, Best for. '
     'Each cell has a short text and a colour-coded dot (green=yes/good, coral=no/different). '
     'Column headers in pastel accent boxes. Sage green for GRPO, dusty blue for RLOO, '
     'lavender for KTO. White background. Clean grid lines. Sans-serif typography.'),

    # ── Chapter 11 ──────────────────────────────────────────────
    ('ch11_fig01_verifiable_vs_learned.png', 3, 11, 1,
     'Verifiable vs Learned Rewards',
     'Two side-by-side panels. Left "Learned Reward Model": prompt and response enter a '
     'neural network box (dusty blue), scalar reward exits, annotation "Can be hacked, '
     'distributional shift". Right "Verifiable Reward": response enters a "Symbolic '
     'Verifier" box (sage green, with checkmark icon), binary correct/wrong exits, '
     'annotation "Ground truth, cannot be gamed". Bold vs divider. White background. '
     'Flat minimal infographic. Crisp arrows.'),

    # ── Chapter 12 ──────────────────────────────────────────────
    ('ch12_fig01_deepseek_phases.png', 3, 12, 1,
     'DeepSeek-R1 Five-Phase Training Pipeline',
     'Horizontal left-to-right pipeline with five numbered stage boxes connected by arrows. '
     '1 "Cold-Start SFT" (sage green) 2 "GRPO Phase 1" (dusty blue) 3 "Rejection '
     'Sampling" (warm coral filter icon) 4 "SFT Phase 2" (sage green) 5 "GRPO Phase 2" '
     '(dusty blue). Above each box a small annotation: model size note. Below each box '
     'a key output (e.g. "structured format", "RL signal", "filtered data"). '
     'White background. Crisp flat infographic. Pastel palette.'),

    ('ch12_fig02_think_answer_format.png', 3, 12, 2,
     'Chain-of-Thought Think/Answer Format',
     'Annotated example output box in light warm grey background. At top: "User: What is '
     '144 divided by 12?". Below: a <think> tag region in soft blue with 3 lines of '
     'reasoning text ending with </think>. Below that: an <answer> tag region in sage '
     'green with "12" and </answer>. Bracket annotations on the right: "Scratchpad '
     '(hidden at inference)" pointing at think region, "Final answer" pointing at answer '
     'region. Clean monospace font for code regions. Minimalist illustration.'),

    # ── Chapter 13 ──────────────────────────────────────────────
    ('ch13_fig01_inference_strategies.png', 3, 13, 1,
     'Test-Time Compute Strategies Compared',
     'Three-panel diagram side by side. Panel 1 "Best-of-N": one prompt with N=4 parallel '
     'arrows to 4 response boxes, best one selected with trophy icon. Panel 2 "Beam Search": '
     'tree structure with branching paths, top-k beams highlighted in dusty blue. '
     'Panel 3 "MCTS": tree with round nodes, UCB scores annotating edges, best path in '
     'coral. Bottom row: compute cost bar (low to high) and accuracy bar (low to high). '
     'White background. Pastel colours. Clean flat infographic.'),

    ('ch13_fig02_scaling_curve.png', 3, 13, 2,
     'Test-Time Compute Scaling Curve',
     'Line chart with horizontal axis "Inference compute (N samples or search depth)" '
     'log scale 1 to 64, vertical axis "Accuracy %" 0 to 100. Three curves: '
     '"Best-of-N" in sage green (rises steeply then plateaus), "Self-consistency" in '
     'dusty blue (similar shape, higher plateau), "MCTS" in coral (slower rise, highest '
     'plateau). Shaded confidence bands. Horizontal dashed line "Training-compute matched". '
     'Clean legend. White background. Sketch-style chart.'),

    # ── Chapter 14 ──────────────────────────────────────────────
    ('ch14_fig01_cai_pipeline.png', 3, 14, 1,
     'Constitutional AI Two-Stage Pipeline',
     'Vertical two-stage diagram. Stage 1 "SL-CAI" (sage green box): (a) Red-team prompt '
     'enters LLM, harmful response generated; (b) LLM self-critiques using constitution '
     'principles; (c) Revised response created; (d) SFT on revised responses. '
     'Stage 2 "RL-CAI" (dusty blue box): Preference pairs from AI feedback -> reward '
     'model -> RL training. Connecting arrow between stages. Constitution scroll icon '
     'on the right. White background. Flat pastel infographic.'),

    # ── Chapter 15 ──────────────────────────────────────────────
    ('ch15_fig01_pareto_frontier.png', 3, 15, 1,
     'Helpfulness vs Safety Pareto Frontier',
     'Scatter plot with horizontal axis "Helpfulness score" 0-100 and vertical axis '
     '"Safety score" 0-100. A smooth convex Pareto frontier curve in dusty blue. '
     'Points below the frontier in light grey labelled "dominated". Three highlighted '
     'Pareto-optimal points: one high-helpfulness (coral dot), one balanced (sage green '
     'dot), one high-safety (lavender dot), each with a small label. Shaded feasible '
     'region below the frontier. Clean axes. White background. Minimalist chart.'),

    # ── Chapter 16 ──────────────────────────────────────────────
    ('ch16_fig01_domain_rl_pipeline.png', 3, 16, 1,
     'Domain-Specific RL Pipeline',
     'Horizontal pipeline with domain selector at left: three domain icons stacked '
     '(Code icon, Math symbol, Tool/wrench icon) each with an arrow merging into a '
     '"Domain-Specific Reward" box in warm coral. Arrow right to "Policy LLM" in dusty '
     'blue. Arrow right to "Verifier / Executor" box (code runner for code, symbolic '
     'checker for math, API call for tools) in sage green. Arrow right looping back '
     'labelled "reward signal". White background. Flat minimal infographic.'),

    # ── Chapter 17 ──────────────────────────────────────────────
    ('ch17_fig01_chatbot_pipeline.png', 4, 17, 1,
     'End-to-End Chatbot Training Pipeline',
     'Horizontal pipeline with 4 stages: (1) "Base LLM" box -> SFT arrow -> (2) "SFT '
     'Model" box (sage green) -> Reward Training arrow -> (3) "Reward Model" box '
     '(dusty blue, scalar output) -> DPO arrow -> (4) "Aligned Chatbot" box (lavender, '
     'chat bubble icon). Below the pipeline a timeline bar showing data needed at each '
     'stage: conversation data, preference pairs, preference pairs. Clean flat icons. '
     'White background. Pastel infographic.'),

    # ── Chapter 18 ──────────────────────────────────────────────
    ('ch18_fig01_reasoner_pipeline.png', 4, 18, 1,
     'Reasoner Training Pipeline',
     'Vertical pipeline: (1) "Base LLM" -> Cold-Start SFT on CoT examples -> '
     '(2) "CoT-Initialised Model" (sage green) -> GRPO with verifiable math/code rewards -> '
     '(3) "Reasoning Policy" (dusty blue, brain icon) -> Best-of-N at inference -> '
     '(4) "Final Answer" (coral, checkmark). Annotations on the right side: '
     '"No human labels needed" beside GRPO stage, "Free accuracy boost" beside best-of-N. '
     'White background. Crisp flat infographic.'),

    # ── Chapter 19 ──────────────────────────────────────────────
    ('ch19_fig01_agent_rl_loop.png', 4, 19, 1,
     'Agent RL Training Loop',
     'Circular loop diagram with five nodes: (1) "Environment / Tools" box (sage green, '
     'wrench icon); (2) "Observation o_t" node; (3) "Agent Policy" circle (dusty blue, '
     'brain icon); (4) "Action a_t" node (tool call, text response, or search); '
     '(5) "Trajectory Reward" box (coral). Clockwise arrows connecting all nodes. '
     'A "KL Constraint" annotation on the policy node. "Multi-step rollout" label '
     'spanning the loop arc. White background. Flat pastel infographic. Clean thin arrows.'),
]

STYLE = {
    'fig_w': 10, 'fig_h': 6.2,
    'bg':       '#FAFAF8',
    'border':   '#BFBAB4',
    'prompt_bg':'#F0EDE8',
    'title_fg': '#2A2825',
    'label_fg': '#6B6560',
    'prompt_fg':'#1E1C1A',
    'font_title': 13,
    'font_label': 9,
    'font_prompt': 8.2,
}


def make_placeholder(fname, part, ch, fig_n, title, prompt):
    accent = PART_COLORS[part]
    fig, ax = plt.subplots(figsize=(STYLE['fig_w'], STYLE['fig_h']))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')

    # Background
    fig.patch.set_facecolor(STYLE['bg'])
    ax.set_facecolor(STYLE['bg'])

    # Outer border
    border = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                             boxstyle='round,pad=0.01',
                             linewidth=1.4, edgecolor=STYLE['border'],
                             facecolor=STYLE['bg'])
    ax.add_patch(border)

    # Accent header bar
    header = FancyBboxPatch((0.02, 0.84), 0.96, 0.13,
                             boxstyle='round,pad=0.01',
                             linewidth=0, edgecolor='none',
                             facecolor=accent + '33')   # 20% alpha
    ax.add_patch(header)

    # Accent left stripe
    stripe = plt.Rectangle((0.02, 0.02), 0.006, 0.82,
                             linewidth=0, facecolor=accent)
    ax.add_patch(stripe)

    # Chapter / figure label
    ax.text(0.06, 0.905,
            f'Chapter {ch}  ·  Figure {fig_n}  ·  Part {part}',
            fontsize=STYLE['font_label'], color=accent,
            fontweight='bold', va='center', transform=ax.transAxes,
            fontfamily='monospace')

    # Figure title
    ax.text(0.06, 0.855,
            title,
            fontsize=STYLE['font_title'], color=STYLE['title_fg'],
            fontweight='bold', va='center', transform=ax.transAxes)

    # Divider line
    ax.axhline(y=0.83, xmin=0.03, xmax=0.97,
               color=STYLE['border'], linewidth=0.8, linestyle='--')

    # "AI GENERATION PROMPT" label
    ax.text(0.06, 0.775,
            'AI IMAGE GENERATION PROMPT',
            fontsize=7.5, color=accent, fontweight='bold',
            va='center', transform=ax.transAxes,
            fontfamily='monospace')

    # Prompt box
    prompt_box = FancyBboxPatch((0.04, 0.12), 0.92, 0.63,
                                 boxstyle='round,pad=0.015',
                                 linewidth=0.8, edgecolor=STYLE['border'],
                                 facecolor=STYLE['prompt_bg'])
    ax.add_patch(prompt_box)

    # Prompt text (wrapped)
    wrapped = textwrap.fill(prompt, width=105)
    ax.text(0.50, 0.435,
            wrapped,
            fontsize=STYLE['font_prompt'], color=STYLE['prompt_fg'],
            va='center', ha='center', transform=ax.transAxes,
            linespacing=1.55,
            fontfamily='monospace',
            wrap=True)

    # Bottom watermark
    ax.text(0.50, 0.055,
            'PLACEHOLDER  ·  Replace with generated image  ·  '
            f'{fname}',
            fontsize=6.5, color=STYLE['label_fg'],
            va='center', ha='center', transform=ax.transAxes,
            style='italic')

    out_path = os.path.join(OUT, fname)
    plt.savefig(out_path, dpi=150, bbox_inches='tight',
                facecolor=STYLE['bg'])
    plt.close(fig)
    return out_path


generated = []
for row in FIGURES:
    path = make_placeholder(*row)
    generated.append((row[0], row[2], row[3], row[4]))   # fname, ch, fig_n, title
    print(f'  OK  {row[0]}')

print(f'\nGenerated {len(generated)} placeholder images -> chapters/images/')
