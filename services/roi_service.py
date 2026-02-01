def enrich_roi_dataframe(df, what_if_multiplier):
    df["what_if_automation_cost"] = (
        df["automation_testing_cost"] * what_if_multiplier
    )

    df["what_if_roi"] = (
        (df["manual_testing_cost"] - df["what_if_automation_cost"])
        / df["what_if_automation_cost"]
    ) * 100

    df["automation_recommended"] = (
        (df["roi_percentage"] > 0)
        & (df["automation_suitability_score"] >= 60)
    )

    df["estimation_confidence"] = (
        100
        - (df["automation_maintenance_time_per_cycle_hrs"] * 10)
        - (df["automation_dev_time_per_test_hrs"] * 5)
    ).clip(50, 95)

    return df
