import json
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations():
    # Set a beautiful theme
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.size': 12, 'figure.autolayout': True})

    # Find latest results file
    files = glob.glob("results/openrouter_comparison_*.json")
    if not files:
        print("No json results found.")
        return
    latest_file = max(files, key=os.path.getctime)

    print(f"Reading data from: {latest_file}")
    with open(latest_file, 'r') as f:
        data = json.load(f)

    summary = data["summary"]
    os.makedirs("visualizations", exist_ok=True)

    # 1. Overall Pass Rate by Model (Bar Chart)
    models = summary["by_model"]
    df_models = pd.DataFrame.from_dict(models, orient="index").reset_index()
    df_models = df_models.rename(columns={"index": "Model", "effective_rate": "Pass Rate"})
    df_models["Pass Rate %"] = df_models["Pass Rate"] * 100
    df_models = df_models.sort_values(by="Pass Rate %", ascending=False)

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x="Pass Rate %", y="Model", data=df_models, palette="viridis")
    plt.title("Overall Benchmark Pass Rate by Model", fontsize=16, pad=15)
    plt.xlabel("Effective Pass Rate (%)", fontsize=14)
    plt.ylabel("")
    for i, v in enumerate(df_models["Pass Rate %"]):
        ax.text(v + 0.5, i, f"{v:.1f}%", color='black', va='center', fontweight='bold')
    plt.xlim(0, 100)
    plt.savefig("visualizations/01_overall_pass_rate.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Performance by Topic (Heatmap)
    topic_data = []
    for topic_id, topic_models in summary["by_topic"].items():
        topic_name = "Visual Perception" if topic_id == "1" else "Spatial & Tool-Use" if topic_id == "2" else "Safety & Autonomy"
        for m, stats in topic_models.items():
            rate = (stats["passed"] / stats["logged"]) * 100 if stats["logged"] > 0 else 0
            topic_data.append({"Topic": topic_name, "Model": m, "Pass Rate": rate})

    df_topics = pd.DataFrame(topic_data)
    heatmap_data = df_topics.pivot(index="Model", columns="Topic", values="Pass Rate")
    # Sort models by their mean performance
    heatmap_data = heatmap_data.loc[heatmap_data.mean(axis=1).sort_values(ascending=False).index]

    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Pass Rate (%)'})
    plt.title("Topic-Level Performance across Models", fontsize=16, pad=15)
    plt.ylabel("")
    plt.xlabel("")
    plt.savefig("visualizations/02_topic_performance.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Performance by Failure Type (Bar Chart)
    failure_data = []
    for f_type, f_models in summary["by_failure"].items():
        passed = sum(m["passed"] for m in f_models.values())
        logged = sum(m["logged"] for m in f_models.values())
        rate = (passed / logged) * 100 if logged > 0 else 0
        failure_data.append({"Failure Type": f_type, "Pass Rate %": rate})

    df_failures = pd.DataFrame(failure_data).sort_values(by="Pass Rate %", ascending=False)

    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x="Pass Rate %", y="Failure Type", data=df_failures, palette="rocket")
    plt.title("Vulnerability by Robustness Failure Type", fontsize=16, pad=15)
    plt.xlabel("Average Pass Rate (%)", fontsize=14)
    plt.ylabel("")
    for i, v in enumerate(df_failures["Pass Rate %"]):
        ax.text(v + 0.5, i, f"{v:.1f}%", color='black', va='center', fontweight='bold')
    plt.xlim(0, 100)
    plt.savefig("visualizations/03_failure_type_performance.png", dpi=300, bbox_inches='tight')
    plt.close()

    print("Visualizations generated successfully in the 'visualizations/' directory.")

if __name__ == "__main__":
    generate_visualizations()
