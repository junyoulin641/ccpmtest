"""
ChartBuilder module for creating matplotlib charts.

Provides static methods to generate various chart types from pandas DataFrames.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Optional


class ChartBuilder:
    """
    Utility class for creating matplotlib charts from pandas DataFrames.

    Provides static methods for generating line, bar, scatter, and pie charts
    with customization options.
    """

    @staticmethod
    def create_line_chart(
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: Optional[str] = None,
        color: Optional[str] = None,
        **kwargs
    ) -> Figure:
        """
        Create a line chart.

        Args:
            df: DataFrame containing the data
            x_col: Column name for X axis
            y_col: Column name for Y axis
            title: Optional custom title
            color: Optional line color
            **kwargs: Additional matplotlib plot arguments

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # Prepare data
        x_data = df[x_col]
        y_data = df[y_col]

        # Plot
        plot_kwargs = kwargs.copy()
        if color:
            plot_kwargs['color'] = color
        plot_kwargs.setdefault('linewidth', 2)
        plot_kwargs.setdefault('marker', 'o')
        plot_kwargs.setdefault('markersize', 4)

        ax.plot(x_data, y_data, **plot_kwargs)

        # Labels and title
        ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
        ax.set_title(
            title if title else f'{y_col} vs {x_col}',
            fontsize=14,
            fontweight='bold',
            pad=20
        )

        # Styling
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        fig.tight_layout()
        return fig

    @staticmethod
    def create_bar_chart(
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: Optional[str] = None,
        color: Optional[str] = None,
        **kwargs
    ) -> Figure:
        """
        Create a bar chart.

        Args:
            df: DataFrame containing the data
            x_col: Column name for X axis (categories)
            y_col: Column name for Y axis (values)
            title: Optional custom title
            color: Optional bar color
            **kwargs: Additional matplotlib bar arguments

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # Limit categories if too many
        if len(df) > 50:
            # Aggregate or take top 50
            df = df.nlargest(50, y_col)

        x_data = df[x_col]
        y_data = df[y_col]

        # Plot
        plot_kwargs = kwargs.copy()
        if color:
            plot_kwargs['color'] = color
        else:
            plot_kwargs['color'] = '#3498db'
        plot_kwargs.setdefault('alpha', 0.8)
        plot_kwargs.setdefault('edgecolor', 'black')
        plot_kwargs.setdefault('linewidth', 0.5)

        ax.bar(range(len(x_data)), y_data, **plot_kwargs)

        # Labels and title
        ax.set_xticks(range(len(x_data)))
        ax.set_xticklabels(x_data, rotation=45, ha='right')
        ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
        ax.set_title(
            title if title else f'{y_col} by {x_col}',
            fontsize=14,
            fontweight='bold',
            pad=20
        )

        # Styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.grid(True, alpha=0.3, linestyle='--')

        fig.tight_layout()
        return fig

    @staticmethod
    def create_scatter_chart(
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        title: Optional[str] = None,
        color: Optional[str] = None,
        **kwargs
    ) -> Figure:
        """
        Create a scatter plot.

        Args:
            df: DataFrame containing the data
            x_col: Column name for X axis
            y_col: Column name for Y axis
            title: Optional custom title
            color: Optional point color
            **kwargs: Additional matplotlib scatter arguments

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        # Downsample if too many points
        plot_df = df
        if len(df) > 10000:
            plot_df = df.sample(n=10000, random_state=42)

        x_data = plot_df[x_col]
        y_data = plot_df[y_col]

        # Plot
        plot_kwargs = kwargs.copy()
        if color:
            plot_kwargs['color'] = color
        else:
            plot_kwargs['color'] = '#e74c3c'
        plot_kwargs.setdefault('alpha', 0.6)
        plot_kwargs.setdefault('s', 50)  # marker size
        plot_kwargs.setdefault('edgecolors', 'black')
        plot_kwargs.setdefault('linewidths', 0.5)

        ax.scatter(x_data, y_data, **plot_kwargs)

        # Labels and title
        ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
        ax.set_title(
            title if title else f'{y_col} vs {x_col}',
            fontsize=14,
            fontweight='bold',
            pad=20
        )

        # Styling
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Add note if downsampled
        if len(df) > 10000:
            ax.text(
                0.02, 0.98,
                f'Showing 10,000 of {len(df):,} points',
                transform=ax.transAxes,
                fontsize=10,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            )

        fig.tight_layout()
        return fig

    @staticmethod
    def create_pie_chart(
        df: pd.DataFrame,
        labels_col: str,
        values_col: str,
        title: Optional[str] = None,
        **kwargs
    ) -> Figure:
        """
        Create a pie chart.

        Args:
            df: DataFrame containing the data
            labels_col: Column name for slice labels
            values_col: Column name for slice values
            title: Optional custom title
            **kwargs: Additional matplotlib pie arguments

        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        # Limit slices if too many
        plot_df = df.copy()
        if len(plot_df) > 20:
            # Keep top 19 and aggregate rest as "Other"
            plot_df = plot_df.nlargest(19, values_col)
            other_value = df[~df[labels_col].isin(plot_df[labels_col])][values_col].sum()
            if other_value > 0:
                other_row = pd.DataFrame({
                    labels_col: ['Other'],
                    values_col: [other_value]
                })
                plot_df = pd.concat([plot_df, other_row], ignore_index=True)

        labels = plot_df[labels_col]
        values = plot_df[values_col]

        # Plot
        plot_kwargs = kwargs.copy()
        plot_kwargs.setdefault('autopct', '%1.1f%%')
        plot_kwargs.setdefault('startangle', 90)
        plot_kwargs.setdefault('counterclock', False)

        # Use a nice color palette
        if 'colors' not in plot_kwargs:
            colors = plt.cm.Set3(range(len(labels)))
            plot_kwargs['colors'] = colors

        wedges, texts, autotexts = ax.pie(values, labels=labels, **plot_kwargs)

        # Make percentage text bold
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        # Title
        ax.set_title(
            title if title else f'Distribution of {values_col}',
            fontsize=14,
            fontweight='bold',
            pad=20
        )

        fig.tight_layout()
        return fig

    @staticmethod
    def validate_chart_data(
        df: pd.DataFrame,
        chart_type: str,
        x_col: str,
        y_col: str
    ) -> tuple[bool, str]:
        """
        Validate data for chart generation.

        Args:
            df: DataFrame to validate
            chart_type: Type of chart ('Line', 'Bar', 'Scatter', 'Pie')
            x_col: X axis column name
            y_col: Y axis column name

        Returns:
            Tuple of (is_valid, error_message)
        """
        if df is None or df.empty:
            return False, "No data available"

        if x_col not in df.columns:
            return False, f"Column '{x_col}' not found in data"

        if y_col not in df.columns:
            return False, f"Column '{y_col}' not found in data"

        # Check for required data types
        if chart_type in ['Line', 'Scatter']:
            if not pd.api.types.is_numeric_dtype(df[y_col]):
                return False, f"'{y_col}' must be numeric for {chart_type} charts"

            if chart_type == 'Scatter':
                if not pd.api.types.is_numeric_dtype(df[x_col]):
                    return False, f"'{x_col}' must be numeric for Scatter charts"

        elif chart_type == 'Bar':
            if not pd.api.types.is_numeric_dtype(df[y_col]):
                return False, f"'{y_col}' must be numeric for Bar charts"

            # Check category count
            unique_cats = df[x_col].nunique()
            if unique_cats > 100:
                return False, f"Too many categories ({unique_cats}). Bar charts work best with <100 categories"

        elif chart_type == 'Pie':
            if not pd.api.types.is_numeric_dtype(df[y_col]):
                return False, f"'{y_col}' must be numeric for Pie charts"

            # Check for negative values
            if (df[y_col] < 0).any():
                return False, "Pie charts cannot display negative values"

            # Check slice count
            unique_slices = df[x_col].nunique()
            if unique_slices > 50:
                return False, f"Too many slices ({unique_slices}). Pie charts work best with <50 slices"

        # Check for sufficient data
        if len(df) < 2:
            return False, "Need at least 2 data points to create a chart"

        return True, ""
