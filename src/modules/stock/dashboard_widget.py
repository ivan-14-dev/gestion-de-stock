from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QVBoxLayout as QVLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from collections import defaultdict
from ...common.models import products, categories, suppliers, movements

# Apply very modern SaaS chart styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'figure.facecolor': '#F9FAFB',
    'axes.facecolor': '#FFFFFF',
    'axes.edgecolor': '#E5E7EB',
    'axes.labelcolor': '#374151',
    'text.color': '#111827',
    'xtick.color': '#6B7280',
    'ytick.color': '#6B7280',
    'grid.color': '#F3F4F6',
    'grid.alpha': 0.4,
    'grid.linewidth': 0.8,
    'lines.linewidth': 3,
    'lines.markersize': 8,
    'lines.marker': 'o',
    'lines.markeredgecolor': '#2563EB',
    'lines.markerfacecolor': '#FFFFFF',
    'lines.markeredgewidth': 2.5,
    'axes.prop_cycle': plt.cycler(color=['#2563EB', '#6B7280', '#22C55E', '#F59E0B', '#EF4444']),
    'font.family': 'sans-serif',
    'font.sans-serif': ['Inter', 'Roboto', 'DejaVu Sans'],
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.titleweight': '700',
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'figure.titleweight': '700',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.spines.bottom': True,
    'axes.spines.left': True,
})

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

        # Pie chart with toolbar
        pie_layout = QVLayout()
        self.pie_canvas = FigureCanvas(Figure())
        pie_toolbar = NavigationToolbar(self.pie_canvas, self)
        pie_layout.addWidget(self.pie_canvas)
        pie_layout.addWidget(pie_toolbar)
        charts_layout.addLayout(pie_layout, 0, 0)

        # Bar chart with toolbar
        bar_layout = QVLayout()
        self.bar_canvas = FigureCanvas(Figure())
        bar_toolbar = NavigationToolbar(self.bar_canvas, self)
        bar_layout.addWidget(self.bar_canvas)
        bar_layout.addWidget(bar_toolbar)
        charts_layout.addLayout(bar_layout, 0, 1)

        # Line chart with toolbar
        line_layout = QVLayout()
        self.line_canvas = FigureCanvas(Figure())
        line_toolbar = NavigationToolbar(self.line_canvas, self)
        line_layout.addWidget(self.line_canvas)
        line_layout.addWidget(line_toolbar)
        charts_layout.addLayout(line_layout, 1, 0)

        # Heatmap with toolbar
        heatmap_layout = QVLayout()
        self.heatmap_canvas = FigureCanvas(Figure())
        heatmap_toolbar = NavigationToolbar(self.heatmap_canvas, self)
        heatmap_layout.addWidget(self.heatmap_canvas)
        heatmap_layout.addWidget(heatmap_toolbar)
        charts_layout.addLayout(heatmap_layout, 1, 1)

        # Doughnut chart with toolbar
        doughnut_layout = QVLayout()
        self.doughnut_canvas = FigureCanvas(Figure())
        doughnut_toolbar = NavigationToolbar(self.doughnut_canvas, self)
        doughnut_layout.addWidget(self.doughnut_canvas)
        doughnut_layout.addWidget(doughnut_toolbar)
        charts_layout.addLayout(doughnut_layout, 2, 0)

        # Horizontal bar chart with toolbar
        hbar_layout = QVLayout()
        self.hbar_canvas = FigureCanvas(Figure())
        hbar_toolbar = NavigationToolbar(self.hbar_canvas, self)
        hbar_layout.addWidget(self.hbar_canvas)
        hbar_layout.addWidget(hbar_toolbar)
        charts_layout.addLayout(hbar_layout, 2, 1)

        # Timeline with toolbar
        timeline_layout = QVLayout()
        self.timeline_canvas = FigureCanvas(Figure())
        timeline_toolbar = NavigationToolbar(self.timeline_canvas, self)
        timeline_layout.addWidget(self.timeline_canvas)
        timeline_layout.addWidget(timeline_toolbar)
        charts_layout.addLayout(timeline_layout, 3, 0, 1, 2)

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

        self.pie_canvas.figure.clear()
        ax = self.pie_canvas.figure.add_subplot(111)
        if cat_stock:
            colors = ['#2563EB', '#6B7280', '#22C55E', '#F59E0B', '#EF4444'][:len(cat_stock)]
            wedges, texts, autotexts = ax.pie(cat_stock.values(), labels=cat_stock.keys(), autopct='%1.1f%%', colors=colors, startangle=90, wedgeprops={'edgecolor': '#FFFFFF', 'linewidth': 2}, pctdistance=0.85)
            # Style the percentage texts
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        ax.set_title("Stock par catégorie", pad=20, fontweight='bold')
        self.pie_canvas.draw()

        # Bar chart: stock by color (top 10)
        color_stock = defaultdict(int)
        for p in products:
            for v in p.variants:
                color_stock[v.color] += v.quantity

        top_colors = sorted(color_stock.items(), key=lambda x: x[1], reverse=True)[:10]
        colors, qtys = zip(*top_colors) if top_colors else ([], [])

        self.bar_canvas.figure.clear()
        ax = self.bar_canvas.figure.add_subplot(111)
        bars = ax.bar(colors, qtys, color='#2563EB', edgecolor='#FFFFFF', linewidth=1, width=0.8)
        ax.set_title("Stock par couleur (top 10)", pad=20, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3)
        # Add value labels on bars
        for bar, qty in zip(bars, qtys):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(qtys)*0.01, str(qty), ha='center', va='bottom', fontweight='bold', fontsize=10)
        self.bar_canvas.draw()

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
            dates.append(m.date)
            totals.append(current_total)

        self.line_canvas.figure.clear()
        ax = self.line_canvas.figure.add_subplot(111)
        if dates:
            ax.plot(dates, totals, marker='o', markersize=6, markerfacecolor='#FFFFFF', markeredgecolor='#2563EB', markeredgewidth=2, linewidth=2.5, color='#2563EB', label='Stock total')
            ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
        ax.set_title("Évolution stock", pad=20, fontweight='bold')
        ax.grid(True, alpha=0.3)
        self.line_canvas.draw()

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

        self.heatmap_canvas.figure.clear()
        ax = self.heatmap_canvas.figure.add_subplot(111)
        if heatmap_data:
            cax = ax.imshow(heatmap_data, cmap='RdYlGn_r', aspect='auto')
            ax.set_xticks(range(len(colors_list)))
            ax.set_xticklabels(colors_list)
            ax.set_yticks(range(len(sizes)))
            ax.set_yticklabels(sizes)
            self.heatmap_canvas.figure.colorbar(cax)
        ax.set_title("Heatmap taille/couleur", pad=20, fontweight='bold')
        self.heatmap_canvas.draw()

        # Doughnut chart: stock by supplier
        sup_stock = defaultdict(int)
        for p in products:
            sup_name = next((s.name for s in suppliers if s.id == p.supplier_id), "Autre")
            qty = sum(v.quantity for v in p.variants)
            sup_stock[sup_name] += qty

        self.doughnut_canvas.figure.clear()
        ax = self.doughnut_canvas.figure.add_subplot(111)
        if sup_stock:
            colors = ['#2563EB', '#6B7280', '#22C55E', '#F59E0B', '#EF4444'][:len(sup_stock)]
            wedges, texts, autotexts = ax.pie(sup_stock.values(), labels=sup_stock.keys(), autopct='%1.1f%%', colors=colors, pctdistance=0.85, startangle=90, wedgeprops={'edgecolor': '#FFFFFF', 'linewidth': 2})
            centre_circle = plt.Circle((0,0),0.70,fc='#F9FAFB', edgecolor='#E5E7EB', linewidth=2)
            ax.add_artist(centre_circle)
            # Add center text
            ax.text(0, 0, 'Fournisseurs', ha='center', va='center', fontsize=12, fontweight='bold', color='#374151')
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        ax.set_title("Stock par fournisseur (doughnut)", pad=20, fontweight='bold')
        self.doughnut_canvas.draw()

        # Horizontal bar chart: top stocked products
        prod_stock = [(p.name, sum(v.quantity for v in p.variants)) for p in products]
        prod_stock.sort(key=lambda x: x[1], reverse=True)
        top_prods = prod_stock[:10]
        names, qtys = zip(*top_prods) if top_prods else ([], [])

        self.hbar_canvas.figure.clear()
        ax = self.hbar_canvas.figure.add_subplot(111)
        bars = ax.barh(names, qtys, color='#2563EB', edgecolor='#FFFFFF', linewidth=1, height=0.8)
        ax.set_title("Top produits stockés", pad=20, fontweight='bold')
        ax.grid(True, axis='x', alpha=0.3)
        # Add value labels on bars
        for bar, qty in zip(bars, qtys):
            ax.text(bar.get_width() + max(qtys)*0.01, bar.get_y() + bar.get_height()/2, str(qty), ha='left', va='center', fontweight='bold', fontsize=10)
        self.hbar_canvas.draw()

        # Timeline: recent movements
        recent_movements = sorted(movements, key=lambda x: x.date, reverse=True)[:20]
        dates = [m.date for m in reversed(recent_movements)]
        types = [m.type for m in reversed(recent_movements)]
        qtys = [m.quantity if m.type == 'in' else -m.quantity for m in reversed(recent_movements)]

        self.timeline_canvas.figure.clear()
        ax = self.timeline_canvas.figure.add_subplot(111)
        ax.plot(dates, qtys, marker='o', markersize=6, markerfacecolor='#FFFFFF', markeredgecolor='#2563EB', markeredgewidth=2, linewidth=2.5, color='#2563EB', label='Mouvements')
        ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
        ax.set_title("Timeline mouvements récents", pad=20, fontweight='bold')
        ax.grid(True, alpha=0.3)
        self.timeline_canvas.draw()