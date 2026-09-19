# canvas_benchmark_analysis.R
# Loads agent_spatial_benchmark_run1.csv and agent_spatial_benchmark_run2.csv.
# Each file holds TRIAL-LEVEL rows (6 trials per stack, per run), so the first
# step is to aggregate to one mean value per stack/metric before comparing runs.
# Then: pivots to long format, computes per-stack per-metric delta between runs,
# plots a grouped bar chart (ggplot2, faceted by metric) with run1 vs run2 bars,
# annotates any stack/metric pair where |run1 - run2| > 15,
# saves the chart, and prints a delta summary table to console.

library(tidyverse)

run1_trials <- read.csv("agent_spatial_benchmark_run1.csv")
run2_trials <- read.csv("agent_spatial_benchmark_run2.csv")

metric_cols <- c("spatial_accuracy_pct", "dep_resolution_hit_rate_pct",
                  "page_nav_success_pct", "avg_layout_latency_ms")

# Aggregate trial-level rows to one mean per stack per metric
run1 <- run1_trials %>%
  group_by(stack_id, stack_name) %>%
  summarise(across(all_of(metric_cols), mean), .groups = "drop")

run2 <- run2_trials %>%
  group_by(stack_id, stack_name) %>%
  summarise(across(all_of(metric_cols), mean), .groups = "drop")

run1_long <- run1 %>%
  pivot_longer(cols = all_of(metric_cols),
               names_to = "metric", values_to = "value") %>%
  mutate(run = "run1")

run2_long <- run2 %>%
  pivot_longer(cols = all_of(metric_cols),
               names_to = "metric", values_to = "value") %>%
  mutate(run = "run2")

combined <- bind_rows(run1_long, run2_long)

delta_table <- combined %>%
  pivot_wider(names_from = run, values_from = value) %>%
  mutate(delta = abs(run1 - run2),
         diverges = delta > 15)

print(delta_table)

p <- ggplot(combined, aes(x = stack_name, y = value, fill = run)) +
  geom_col(position = "dodge") +
  facet_wrap(~ metric, scales = "free_y") +
  geom_text(
    data = delta_table %>% filter(diverges),
    aes(x = stack_name, y = pmax(run1, run2), label = paste0("Δ", round(delta))),
    inherit.aes = FALSE, vjust = -0.5
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 30, hjust = 1)) +
  labs(title = "Benchmark Run 1 vs Run 2 by Stack and Metric",
       x = "Stack", y = "Value")

# Review/adjust label placement in the RStudio Plots pane before exporting.
ggsave("benchmark_comparison_annotated.png", plot = p, width = 10, height = 7, dpi = 150)
