from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QVBoxLayout as QVLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from collections import defaultdict
from ...common.models import products, categories, suppliers, movements


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Summary cards
        cards_layout = QHBoxLayout()
        layout.addLayout(cards_layout)

        self.total_value_label = QLabel("Valeur totale: 0 €")
        self.total_value_label.setStyleSheet("""
            background-color: white;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px;
            font-size: 14px;
            font-weight: 600;
            color: #111827;
        """)
        cards_layout.addWidget(self.total_value_label)

        self.product_count_label = QLabel("Nombre produits: 0")
        self.product_count_label.setStyleSheet("""
            background-color: white;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px;
            font-size: 14px;
            font-weight: 600;
            color: #111827;
        """)
        cards_layout.addWidget(self.product_count_label)

        self.low_stock_label = QLabel("Stock faible: 0")
        self.low_stock_label.setStyleSheet("""
            background-color: white;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px;
            font-size: 14px;
            font-weight: 600;
            color: #111827;
        """)
        cards_layout.addWidget(self.low_stock_label)

        # Charts
        charts_layout = QGridLayout()
        charts_layout.setSpacing(30)  # Add space between charts
        layout.addLayout(charts_layout)

        self.pie_view = QWebEngineView()
        charts_layout.addWidget(self.pie_view, 0, 0)

        self.bar_view = QWebEngineView()
        charts_layout.addWidget(self.bar_view, 0, 1)

        self.line_view = QWebEngineView()
        charts_layout.addWidget(self.line_view, 1, 0)

        self.heatmap_view = QWebEngineView()
        charts_layout.addWidget(self.heatmap_view, 1, 1)

        self.doughnut_view = QWebEngineView()
        charts_layout.addWidget(self.doughnut_view, 2, 0)

        self.hbar_view = QWebEngineView()
        charts_layout.addWidget(self.hbar_view, 2, 1)

        self.timeline_view = QWebEngineView()
        charts_layout.addWidget(self.timeline_view, 3, 0, 1, 2)

        self.update_dashboard()

    def update_dashboard(self):
        # Calculate summaries
        total_value = sum(p.price * sum(v.quantity for v in p.variants) for p in products)
        self.total_value_label.setText(f"Valeur totale: {total_value:.2f} €")

        self.product_count_label.setText(f"Nombre produits: {len(products)}")

        low_stock = sum(1 for p in products if sum(v.quantity for v in p.variants) < 10)  # Assume threshold 10
        self.low_stock_label.setText(f"Stock faible: {low_stock}")

        # Pie chart: stock by category
        cat_stock = defaultdict(int)
        for p in products:
            cat_name = next((c.name for c in categories if c.id == p.category_id), "Autre")
            qty = sum(v.quantity for v in p.variants)
            cat_stock[cat_name] += qty

        if cat_stock:
            colors = ['#2563EB', '#6B7280', '#22C55E', '#F59E0B', '#EF4444'][:len(cat_stock)]
            fig = go.Figure(data=[go.Pie(labels=list(cat_stock.keys()), values=list(cat_stock.values()), marker_colors=colors, textinfo='label+percent', insidetextorientation='radial')])
            fig.update_layout(title="Stock par catégorie", title_font=dict(size=16, family='Inter', color='#111827'), paper_bgcolor='#F9FAFB', plot_bgcolor='#FFFFFF')
            self.pie_view.setHtml(fig.to_html(include_plotlyjs='cdn', full_html=False))
        else:
            self.pie_view.setHtml("<p>No data</p>")

        # Bar chart: stock by color (top 10)
        color_stock = defaultdict(int)
        for p in products:
            for v in p.variants:
                color_stock[v.color] += v.quantity

        top_colors = sorted(color_stock.items(), key=lambda x: x[1], reverse=True)[:10]
        colors, qtys = zip(*top_colors) if top_colors else ([], [])

        if colors:
            fig = go.Figure(data=[go.Bar(x=list(colors), y=list(qtys), marker_color='#2563EB', marker_line_color='#FFFFFF', marker_line_width=1)])
            fig.update_layout(title="Stock par couleur (top 10)", title_font=dict(size=16, family='Inter', color='#111827'), paper_bgcolor='#F9FAFB', plot_bgcolor='#FFFFFF', xaxis_title="Couleur", yaxis_title="Quantité")
            fig.update_traces(text=list(qtys), textposition='outside')
            self.bar_view.setHtml(fig.to_html(include_plotlyjs='cdn', full_html=False))
        else:
            self.bar_view.setHtml("<p>No data</p>")

        # Line chart: stock evolution (simplified, assume daily totals from movements)
        # For simplicity, plot cumulative
        dates = []
        totals = []
        current_total = 0
        for m in sorted(movements, key=lambda x: x.date):
            if m.type == 'in':
                current_total += m.quantity
            elif m.type == 'out':
                current_total -= m.quantity
            dates.append(str(m.date))
            totals.append(current_total)

        if dates:
            fig = go.Figure(data=[go.Scatter(x=dates, y=totals, mode='lines+markers', marker=dict(size=8, color='#2563EB', line=dict(width=2, color='#FFFFFF')), line=dict(width=3, color='#2563EB'), name='Stock total')])
            fig.update_layout(title="Évolution stock", title_font=dict(size=16, family='Inter', color='#111827'), paper_bgcolor='#F9FAFB', plot_bgcolor='#FFFFFF', xaxis_title="Date", yaxis_title="Quantité totale")
            self.line_view.setHtml(fig.to_html(include_plotlyjs='cdn', full_html=False))
        else:
            self.line_view.setHtml("<p>No data</p>")

        # Heatmap: size vs color
        sizes = set()
        colors_set = set()
        for p in products:
            for v in p.variants:
                sizes.add(v.size)
                colors_set.add(v.color)

        sizes = sorted(list(sizes))
        colors_list = sorted(list(colors_set))
        heatmap_data = [[0 for _ in colors_list] for _ in sizes]

        for p in products:
            for v in p.variants:
                if v.size in sizes and v.color in colors_list:
                    i = sizes.index(v.size)
                    j = colors_list.index(v.color)
                    heatmap_data[i][j] += v.quantity

        if heatmap_data:
            fig = go.Figure(data=go.Heatmap(z=heatmap_data, x=colors_list, y=sizes, colorscale='RdYlGn_r'))
            fig.update_layout(title="Heatmap taille/couleur", title_font=dict(size=16, family='Inter', color='#111827'), paper_bgcolor='#F9FAFB', plot_bgcolor='#FFFFFF', xaxis_title="Couleur", yaxis_title="Taille")
            self.heatmap_view.setHtml(fig.to_html(include_plotlyjs='cdn', full_html=False))
        else:
            self.heatmap_view.setHtml("<p>No data</p>")

        # Doughnut chart: stock by supplier
        sup_stock = defaultdict(int)
        for p in products:
            sup_name = next((s.name for s in suppliers if s.id == p.supplier_id), "Autre")
            qty = sum(v.quantity for v in p.variants)
            sup_stock[sup_name] += qty

        if sup_stock:
            colors = ['#2563EB', '#6B7280', '#22C55E', '#F59E0B', '#EF4444'][:len(sup_stock)]
            fig = go.Figure(data=[go.Pie(labels=list(sup_stock.keys()), values=list(sup_stock.values()), marker_colors=colors, textinfo='label+percent', hole=0.7)])
            fig.update_layout(title="Stock par fournisseur (doughnut)", title_font=dict(size=16, family='Inter', color='#111827'), paper_bgcolor='#F9FAFB', plot_bgcolor='#FFFFFF', annotations=[dict(text='Fournisseurs', x=0.5, y=0.5, font_size=12, showarrow=False)])
            self.doughnut_view.setHtml(fig.to_html(include_plotlyjs='cdn', full_html=False))
        else:
            self.doughnut_view.setHtml("<p>No data</p>")

        # Horizontal bar chart: top stocked products
        prod_stock = [(p.name, sum(v.quantity for v in p.variants)) for p in products]
        prod_stock.sort(key=lambda x: x[1], reverse=True)
        top_prods = prod_stock[:10]
        names, qtys = zip(*top_prods) if top_prods else ([], [])

        if names:
            fig = go.Figure(data=[go.Bar(y=list(names), x=list(qtys), orientation='h', marker_color='#2563EB', marker_line_color='#FFFFFF', marker_line_width=1)])
            fig.update_layout(title="Top produits stockés", title_font=dict(size=16, family='Inter', color='#111827'), paper_bgcolor='#F9FAFB', plot_bgcolor='#FFFFFF', xaxis_title="Quantité", yaxis_title="Produit")
            fig.update_traces(text=list(qtys), textposition='outside')
            self.hbar_view.setHtml(fig.to_html(include_plotlyjs='cdn', full_html=False))
        else:
            self.hbar_view.setHtml("<p>No data</p>")

        # Timeline: recent movements
        recent_movements = sorted(movements, key=lambda x: x.date, reverse=True)[:20]
        dates = [str(m.date) for m in reversed(recent_movements)]
        qtys = [m.quantity if m.type == 'in' else -m.quantity for m in reversed(recent_movements)]

        if dates:
            fig = go.Figure(data=[go.Scatter(x=dates, y=qtys, mode='lines+markers', marker=dict(size=8, color='#2563EB', line=dict(width=2, color='#FFFFFF')), line=dict(width=3, color='#2563EB'), name='Mouvements')])
            fig.update_layout(title="Timeline mouvements récents", title_font=dict(size=16, family='Inter', color='#111827'), paper_bgcolor='#F9FAFB', plot_bgcolor='#FFFFFF', xaxis_title="Date", yaxis_title="Quantité")
            self.timeline_view.setHtml(fig.to_html(include_plotlyjs='cdn', full_html=False))
        else:
            self.timeline_view.setHtml("<p>No data</p>")