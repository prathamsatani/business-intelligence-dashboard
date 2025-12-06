import gradio as gr
import pandas as pd
from data_processor import (
    load_data,
    get_summary_statistics,
    get_categorical_summary,
    get_missing_values,
    get_correlation_matrix,
    filter_data,
)
from visualizations import (
    create_time_series_plot,
    create_distribution_plot,
    create_bar_chart,
    create_scatter_plot,
)
from insights import (
    get_top_bottom_performers,
    detect_trends,
    detect_anomalies,
)
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

def create_dashboard():
    """Creates and returns the Gradio dashboard."""
    with gr.Blocks() as demo:
        gr.Markdown("# Business Intelligence Dashboard")

        # State variables
        df_state = gr.State(value=None)
        filtered_df_state = gr.State(value=None)

        # ==================== DATA UPLOAD TAB ====================
        with gr.Tab("Data Upload"):
            file_input = gr.File(label="Upload your CSV or Excel file")

            with gr.Row():
                shape_output = gr.Textbox(label="Shape")
                columns_output = gr.Textbox(label="Columns")

            with gr.Row():
                dtypes_output = gr.DataFrame(label="Data Types")
                missing_output = gr.DataFrame(label="Missing Values")

            head_output = gr.DataFrame(label="First 5 rows")
            tail_output = gr.DataFrame(label="Last 5 rows")

        # ==================== STATISTICS TAB ====================
        with gr.Tab("Statistics"):
            stats_btn = gr.Button("Generate Statistics", variant="primary")
            
            gr.Markdown("### Numerical Summary")
            numerical_summary = gr.DataFrame(label="Numerical Summary")
            
            gr.Markdown("### Categorical Summary")
            categorical_summary = gr.DataFrame(label="Categorical Summary")
            
            gr.Markdown("### Missing Values")
            missing_values = gr.DataFrame(label="Missing Values")
            
            gr.Markdown("### Correlation Heatmap")
            correlation_heatmap = gr.Plot(label="Correlation Heatmap")

        # ==================== VISUALIZATIONS TAB ====================
        with gr.Tab("Visualizations"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### Filters")
                    
                    filter_column = gr.Dropdown(
                        label="Filter Column", 
                        choices=[], 
                        interactive=True,
                        allow_custom_value=True  # <-- Added this
                    )
                    
                    filter_type_display = gr.Textbox(
                        label="Filter Type", 
                        value="Select a column first",
                        interactive=False
                    )
                    
                    num_min = gr.Number(
                        label="Min Value", 
                        visible=True, 
                        interactive=True
                    )
                    num_max = gr.Number(
                        label="Max Value", 
                        visible=True, 
                        interactive=True
                    )
                    
                    cat_values = gr.Dropdown(
                        label="Select Values", 
                        choices=[], 
                        multiselect=True,
                        visible=False,
                        interactive=True,
                        allow_custom_value=True  # <-- Added this
                    )
                    
                    date_start = gr.Textbox(
                        label="Start Date (YYYY-MM-DD)",
                        visible=False,
                        interactive=True
                    )
                    date_end = gr.Textbox(
                        label="End Date (YYYY-MM-DD)",
                        visible=False,
                        interactive=True
                    )
                        
                    apply_filter_btn = gr.Button("Apply Filter", variant="primary")
                    reset_filters_btn = gr.Button("Reset Filters")
                    export_csv_btn = gr.Button("Export Filtered Data as CSV")
                    csv_file_output = gr.File(label="Download CSV", visible=True)
                    row_count_output = gr.Textbox(
                        label="Filtered Row Count", 
                        value="No data loaded",
                        interactive=False
                    )

                with gr.Column(scale=3):
                    gr.Markdown("### Filtered Data Preview")
                    filtered_preview = gr.DataFrame(label="Filtered Data (First 10 rows)")
                    
                    gr.Markdown("### Visualizations")
                    with gr.Accordion("Time Series Plot", open=True):
                        with gr.Row():
                            ts_date_col = gr.Dropdown(label="Date Column", choices=[])
                            ts_value_col = gr.Dropdown(label="Value Column", choices=[])
                            ts_color_col = gr.Dropdown(label="Color by (optional)", choices=[])
                        ts_plot = gr.Plot()

                    with gr.Accordion("Distribution Plot", open=True):
                        dist_col = gr.Dropdown(label="Column", choices=[])
                        dist_plot = gr.Plot()

                    with gr.Accordion("Bar Chart", open=True):
                        with gr.Row():
                            bar_cat_col = gr.Dropdown(label="Categorical Column", choices=[])
                            bar_num_col = gr.Dropdown(label="Numerical Column", choices=[])
                            bar_agg = gr.Dropdown(
                                label="Aggregation",
                                choices=["sum", "mean", "count", "median"],
                                value="sum",
                            )
                        bar_plot = gr.Plot()

                    with gr.Accordion("Scatter Plot", open=True):
                        with gr.Row():
                            scatter_x_col = gr.Dropdown(label="X-axis Column", choices=[])
                            scatter_y_col = gr.Dropdown(label="Y-axis Column", choices=[])
                            scatter_color_col = gr.Dropdown(label="Color by (optional)", choices=[])
                        scatter_plot = gr.Plot()

        # ==================== INSIGHTS TAB ====================
        with gr.Tab("Insights"):
            gr.Markdown("### Automated Insights")
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Top/Bottom Performers")
                    insight_col = gr.Dropdown(label="Select Column", choices=[])
                    n_performers = gr.Slider(label="Number", minimum=1, maximum=20, step=1, value=5)
                    sort_order = gr.Radio(choices=["Top", "Bottom"], value="Top")
                    perf_btn = gr.Button("Get Performers")
                    performers_output = gr.DataFrame()

                with gr.Column():
                    gr.Markdown("#### Trend Detection")
                    trend_date_col = gr.Dropdown(label="Date Column", choices=[])
                    trend_value_col = gr.Dropdown(label="Value Column", choices=[])
                    trend_btn = gr.Button("Detect Trends")
                    trend_output = gr.Textbox(label="Trend Analysis", lines=10, max_lines=50, autoscroll=False)

                with gr.Column():
                    gr.Markdown("#### Anomaly Detection")
                    anomaly_col = gr.Dropdown(label="Value Column", choices=[])
                    threshold = gr.Slider(label="Std Dev Threshold", minimum=1, maximum=5, step=0.5, value=2)
                    anomaly_btn = gr.Button("Detect Anomalies")
                    anomaly_output = gr.DataFrame()

        # ====================================================================
        # CALLBACKS - All callbacks defined here after all components exist
        # ====================================================================
        
        # --- Data Upload Callbacks ---
        def process_upload(file):
            if file is None:
                return (None, None, "", "", None, None, None, None, 
                        gr.update(choices=[], value=None))
            try:
                df = load_data(file)
                df = df.loc[:, ~df.columns.duplicated()]
                
                for col in df.columns:
                    if df[col].dtype == "object":
                        try:
                            df[col] = pd.to_datetime(df[col])
                        except (ValueError, TypeError):
                            continue

                shape = str(df.shape)
                columns = ", ".join(df.columns)
                
                dtypes_df = pd.DataFrame({
                    "Column": df.columns,
                    "Data Type": df.dtypes.astype(str).values
                })
                
                missing_df = pd.DataFrame({
                    "Column": df.columns,
                    "Missing Count": df.isnull().sum().values,
                    "Missing %": (df.isnull().sum() / len(df) * 100).round(2).values
                })
                
                filter_choices = gr.update(choices=df.columns.tolist(), value=None)
                
                return (df, df.copy(), shape, columns, dtypes_df, missing_df, 
                        df.head(), df.tail(), filter_choices)
            except Exception as e:
                gr.Warning(f"Error loading file: {str(e)}")
                return (None, None, "", "", None, None, None, None,
                        gr.update(choices=[], value=None))

        file_input.upload(
            process_upload,
            inputs=file_input,
            outputs=[
                df_state,
                filtered_df_state,
                shape_output,
                columns_output,
                dtypes_output,
                missing_output,
                head_output,
                tail_output,
                filter_column,
            ],
        )

        # --- Statistics Callbacks ---
        def generate_statistics(df):
            if df is None:
                gr.Warning("Please upload data first.")
                return None, None, None, None
            
            num_summary = get_summary_statistics(df)
            
            cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
            if cat_cols:
                cat_data = []
                for col in cat_cols:
                    value_counts = df[col].value_counts()
                    for value, count in value_counts.items():
                        pct = round((count / len(df) * 100), 2) if len(df) > 0 else 0
                        cat_data.append({
                            "Column": col,
                            "Value": value,
                            "Count": count,
                            "Percentage %": pct
                        })
                cat_summary_df = pd.DataFrame(cat_data)
            else:
                cat_summary_df = pd.DataFrame({"Message": ["No categorical columns found"]})
            
            missing_df = pd.DataFrame({
                "Column": df.columns,
                "Missing Count": df.isnull().sum().values,
                "Missing %": (df.isnull().sum() / len(df) * 100).round(2).values,
                "Non-Null Count": df.notnull().sum().values
            })
            missing_df = missing_df.sort_values("Missing Count", ascending=False).reset_index(drop=True)
            
            corr_matrix = get_correlation_matrix(df)
            heatmap = (
                px.imshow(
                    corr_matrix, 
                    text_auto=True,
                    title="Correlation Matrix",
                    color_continuous_scale="RdBu_r"
                )
                if corr_matrix is not None and not corr_matrix.empty
                else None
            )
            
            return num_summary, cat_summary_df, missing_df, heatmap

        stats_btn.click(
            generate_statistics,
            inputs=df_state,
            outputs=[numerical_summary, categorical_summary, missing_values, correlation_heatmap],
        )

        # --- Filter Callbacks ---
        def update_filter_ui(df, col):
            if df is None or col is None or col not in df.columns:
                return (
                    gr.update(value="Select a column first"),
                    gr.update(value=None, visible=False),
                    gr.update(value=None, visible=False),
                    gr.update(choices=[], value=[], visible=False),
                    gr.update(value="", visible=False),
                    gr.update(value="", visible=False),
                )
            
            if pd.api.types.is_numeric_dtype(df[col]):
                min_val = float(df[col].min())
                max_val = float(df[col].max())
                return (
                    gr.update(value=f"Numeric Range (min: {min_val:.2f}, max: {max_val:.2f})"),
                    gr.update(value=min_val, visible=True),
                    gr.update(value=max_val, visible=True),
                    gr.update(choices=[], value=[], visible=False),
                    gr.update(value="", visible=False),
                    gr.update(value="", visible=False),
                )
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                min_date = str(df[col].min().date())
                max_date = str(df[col].max().date())
                return (
                    gr.update(value=f"Date Range ({min_date} to {max_date})"),
                    gr.update(value=None, visible=False),
                    gr.update(value=None, visible=False),
                    gr.update(choices=[], value=[], visible=False),
                    gr.update(value=min_date, visible=True),
                    gr.update(value=max_date, visible=True),
                )
            else:
                unique_vals = df[col].dropna().unique().tolist()
                print(unique_vals)
                return (
                    gr.update(value=f"Categorical ({len(unique_vals)} unique values)"),
                    gr.update(value=None, visible=False),
                    gr.update(value=None, visible=False),
                    gr.update(choices=unique_vals, visible=True),
                    gr.update(value="", visible=False),
                    gr.update(value="", visible=False),
                )
        filter_column.change(
            update_filter_ui,
            inputs=[df_state, filter_column],
            outputs=[filter_type_display, num_min, num_max, cat_values, date_start, date_end]
        )

        def apply_single_filter(df, filtered_df, col, min_val, max_val, cat_vals, d_start, d_end):
            if df is None:
                return None, "No data loaded"
            
            working_df = filtered_df if filtered_df is not None else df.copy()
            
            if col is None or col not in working_df.columns:
                return working_df, f"{len(working_df)} rows"
            
            try:
                if pd.api.types.is_numeric_dtype(working_df[col]):
                    if min_val is not None and max_val is not None:
                        working_df = working_df[
                            (working_df[col] >= min_val) & (working_df[col] <= max_val)
                        ]
                elif pd.api.types.is_datetime64_any_dtype(working_df[col]):
                    if d_start and d_end:
                        start = pd.to_datetime(d_start)
                        end = pd.to_datetime(d_end)
                        working_df = working_df[
                            (working_df[col] >= start) & (working_df[col] <= end)
                        ]
                else:
                    if cat_vals and len(cat_vals) > 0:
                        working_df = working_df[working_df[col].isin(cat_vals)]
            except Exception as e:
                gr.Warning(f"Filter error: {str(e)}")
                return filtered_df, "Error applying filter"
            
            return working_df, f"{len(working_df)} rows"

        apply_filter_btn.click(
            apply_single_filter,
            inputs=[df_state, filtered_df_state, filter_column, num_min, num_max, cat_values, date_start, date_end],
            outputs=[filtered_df_state, row_count_output]
        )

        def reset_filters(df):
            if df is None:
                return None, "No data loaded"
            return df.copy(), f"{len(df)} rows (reset)"

        reset_filters_btn.click(
            reset_filters,
            inputs=[df_state],
            outputs=[filtered_df_state, row_count_output]
        )

        # --- Preview and Row Count Callbacks ---
        def update_row_count(df):
            if df is None:
                return "No data loaded"
            return f"{len(df)} rows"

        def update_filtered_preview(df):
            if df is None:
                return None
            return df.head(10)

        df_state.change(update_row_count, inputs=df_state, outputs=row_count_output)
        df_state.change(update_filtered_preview, inputs=df_state, outputs=filtered_preview)
        filtered_df_state.change(update_filtered_preview, inputs=filtered_df_state, outputs=filtered_preview)

        # --- Visualization Dropdown Callbacks ---
        def update_dropdowns_on_upload(df):
            if df is None:
                return tuple(gr.update(choices=[]) for _ in range(9))
            
            num_choices = df.select_dtypes(include=["number"]).columns.tolist()
            cat_choices = df.select_dtypes(include=["object", "category"]).columns.tolist()
            date_choices = df.select_dtypes(include=["datetime"]).columns.tolist()
            
            return (
                gr.update(choices=date_choices),
                gr.update(choices=num_choices),
                gr.update(choices=["None"] + cat_choices),
                gr.update(choices=num_choices),
                gr.update(choices=cat_choices),
                gr.update(choices=num_choices),
                gr.update(choices=num_choices),
                gr.update(choices=num_choices),
                gr.update(choices=["None"] + cat_choices),
            )

        df_state.change(
            update_dropdowns_on_upload,
            inputs=df_state,
            outputs=[
                ts_date_col, ts_value_col, ts_color_col, dist_col,
                bar_cat_col, bar_num_col,
                scatter_x_col, scatter_y_col, scatter_color_col,
            ],
        )

        # --- Plot Update Callbacks ---
        def update_all_plots(df, ts_d, ts_v, ts_c, dist_c, bar_c, bar_n, bar_a, sc_x, sc_y, sc_c):
            if df is None:
                return None, None, None, None
            
            if ts_d and ts_v:
                color_col = ts_c if ts_c and ts_c != "None" else None
                ts_fig = create_time_series_plot(df, ts_d, ts_v, color_col)
            else:
                ts_fig = None
            
            dist_fig = create_distribution_plot(df, dist_c) if dist_c else None
            bar_fig = create_bar_chart(df, bar_c, bar_n, bar_a) if bar_c and bar_n else None
            
            if sc_x and sc_y:
                scatter_color = sc_c if sc_c and sc_c != "None" else None
                scatter_fig = create_scatter_plot(df, sc_x, sc_y, scatter_color)
            else:
                scatter_fig = None
            
            return ts_fig, dist_fig, bar_fig, scatter_fig

        inputs_for_plotting = [
            filtered_df_state,
            ts_date_col, ts_value_col, ts_color_col, dist_col,
            bar_cat_col, bar_num_col, bar_agg,
            scatter_x_col, scatter_y_col, scatter_color_col,
        ]
        outputs_for_plotting = [ts_plot, dist_plot, bar_plot, scatter_plot]
        
        filtered_df_state.change(
            update_all_plots,
            inputs=inputs_for_plotting,
            outputs=outputs_for_plotting,
        )
        
        for component in inputs_for_plotting[1:]:
            component.change(
                update_all_plots,
                inputs=inputs_for_plotting,
                outputs=outputs_for_plotting,
            )

        # --- Export CSV Callback ---
        def export_csv(df):
            if df is not None:
                import tempfile
                import os
                temp_dir = tempfile.gettempdir()
                filepath = os.path.join(temp_dir, "filtered_data.csv")
                df.to_csv(filepath, index=False)
                return gr.File(value=filepath)
            return None

        export_csv_btn.click(export_csv, inputs=[filtered_df_state], outputs=[csv_file_output])

        # --- Insights Dropdown Callbacks ---
        def update_insight_dropdowns(df):
            if df is None:
                return tuple(gr.update(choices=[]) for _ in range(4))
            num_cols = df.select_dtypes(include=["number"]).columns.tolist()
            date_cols = df.select_dtypes(include=["datetime"]).columns.tolist()
            return (
                gr.update(choices=num_cols),
                gr.update(choices=date_cols),
                gr.update(choices=num_cols),
                gr.update(choices=num_cols),
            )

        df_state.change(
            update_insight_dropdowns,
            inputs=df_state,
            outputs=[insight_col, trend_date_col, trend_value_col, anomaly_col],
        )

        # --- Insights Action Callbacks ---
        def safe_get_performers(df, col, n, order):
            if df is None or col is None:
                return pd.DataFrame()
            return get_top_bottom_performers(df, col, int(n), ascending=(order == "Bottom"))

        perf_btn.click(
            safe_get_performers,
            inputs=[filtered_df_state, insight_col, n_performers, sort_order],
            outputs=[performers_output],
        )
        
        def safe_detect_trends(df, date_col, value_col):
            if df is None or date_col is None or value_col is None:
                return "Please upload data and select columns first."
            result = detect_trends(df, date_col, value_col)
            if isinstance(result, str):
                result = result.replace('\\n', '\n')
                result = result.replace('\\t', '\t')
                result = result.replace('\\r', '\r')
                result = result.replace('\\\\', '\\')
            return result

        trend_btn.click(
            safe_detect_trends,
            inputs=[filtered_df_state, trend_date_col, trend_value_col],
            outputs=[trend_output],
        )
        
        def safe_detect_anomalies(df, col, thresh):
            if df is None or col is None:
                return pd.DataFrame()
            return detect_anomalies(df, col, thresh)

        anomaly_btn.click(
            safe_detect_anomalies,
            inputs=[filtered_df_state, anomaly_col, threshold],
            outputs=[anomaly_output],
        )

    return demo


if __name__ == "__main__":
    dashboard = create_dashboard()
    dashboard.launch()