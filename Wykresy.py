# 1. Wykres słupkowy metryk w zależności od prawdopodobieństwa pacjenta
def plot_metrics_vs_prob(model_results):
    metrics = ['recoveries', 'deaths', 'resources_used']
    probabilities = list(model_results.keys())
    data = {metric: [model_results[prob][metric] for prob in probabilities] for metric in metrics}

    for metric, values in data.items():
        plt.figure(figsize=(8, 5))
        sns.barplot(x=probabilities, y=values)
        plt.title(f'{metric.capitalize()} vs Patient Probability')
        plt.xlabel('Patient Probability')
        plt.ylabel(metric.capitalize())
        plt.show()


# 2. Wykres kołowy pacjentów
def plot_pie_chart(patients_by_status):
    labels = list(patients_by_status.keys())
    sizes = [len(patients) for patients in patients_by_status.values()]
    colors = sns.color_palette("pastel")[:len(labels)]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Patient Distribution by Health Status')
    plt.show()


# 3. Testy statystyczne
def perform_statistical_tests(results_model_1, results_model_2):
    # Dane muszą być listami wielu wartości, aby test działał
    recoveries_1 = results_model_1.get('recoveries', [])
    recoveries_2 = results_model_2.get('recoveries', [])

    if len(recoveries_1) < 2 or len(recoveries_2) < 2:
        print("T-test failed: Not enough data for statistical comparison.")
        return

    # Chi-squared Test
    contingency_table = [
        [results_model_1['recoveries'], results_model_1['deaths']],
        [results_model_2['recoveries'], results_model_2['deaths']],
    ]
    chi2, p, _, _ = chi2_contingency(contingency_table)
    print(f"Chi-squared Test: chi2={chi2:.2f}, p-value={p:.4f}")

    # T-test
    try:
        t_stat, p_val = ttest_ind(recoveries_1, recoveries_2)
        print(f"T-test for Recoveries: t-statistic={t_stat:.2f}, p-value={p_val:.4f}")
    except Exception as e:
        print(f"T-test failed: {e}")


#To możliwe że trzeba będzie wyjebać bo to jest ten wykres który nie wyszedł tak jak chcialem 
# 4. Krzywa porównawcza modeli
def compare_models(results_model_1, results_model_2):
    thresholds = np.linspace(0, 1, 100)
    model_1_better = [np.random.random() for _ in thresholds]
    model_2_better = [1 - val for val in model_1_better]

    plt.figure(figsize=(8, 5))
    plt.plot(thresholds, model_1_better, label='Model 1 (Resource Allocation)')
    plt.plot(thresholds, model_2_better, label='Model 2 (Triage)')
    plt.fill_between(thresholds, model_1_better, model_2_better, where=np.array(model_1_better) > np.array(model_2_better), alpha=0.2, color='blue', label='Model 1 Better')
    plt.fill_between(thresholds, model_2_better, model_1_better, where=np.array(model_2_better) > np.array(model_1_better), alpha=0.2, color='orange', label='Model 2 Better')
    plt.title('Model Comparison Curve')
    plt.xlabel('Thresholds')
    plt.ylabel('Model Effectiveness')
    plt.legend()
    plt.show()


# Jakieś wymyślone dane żeby przetestować czy to działa
if __name__ == "__main__":
    # Symulowane dane wyjściowe modeli
    resource_model_results = {
        0.1: {'recoveries': 30, 'deaths': 5, 'resources_used': 50},
        0.2: {'recoveries': 25, 'deaths': 8, 'resources_used': 60},
        0.3: {'recoveries': 20, 'deaths': 10, 'resources_used': 70},
    }

    triage_model_results = {
        0.1: {'recoveries': 28, 'deaths': 7, 'resources_used': 45},
        0.2: {'recoveries': 23, 'deaths': 9, 'resources_used': 55},
        0.3: {'recoveries': 18, 'deaths': 12, 'resources_used': 65},
    }

    # Rysowanie 
    plot_metrics_vs_prob(resource_model_results)
    plot_metrics_vs_prob(triage_model_results)

    patients_by_status = {
        'green': [1] * 50,
        'yellow': [1] * 30,
        'orange': [1] * 15,
        'red': [1] * 5,
    }
    plot_pie_chart(patients_by_status)

    # Testy statystyczne
    perform_statistical_tests(resource_model_results[0.1], triage_model_results[0.1])

    # Krzywa porównawcza
    compare_models(resource_model_results[0.1], triage_model_results[0.1])
