from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import defaultdict
from .models import products, categories, suppliers, movements

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Summary cards
        cards_layout = QHBoxLayout()
        layout.addLayout(cards_layout)

        self.total_value_label = QLabel("Valeur totale: 0 €")
        self.total_value_label.setStyleSheet("border: 1px solid black; padding: 10px;")
        cards_layout.addWidget(self.total_value_label)

        self.product_count_label = QLabel("Nombre produits: 0")
        self.product_count_label.setStyleSheet("border: 1px solid black; padding: 10px;")
        cards_layout.addWidget(self.product_count_label)

        self.low_stock_label = QLabel("Stock faible: 0")
        self.low_stock_label.setStyleSheet("border: 1px solid black; padding: 10px;")
        cards_layout.addWidget(self.low_stock_label)

        # Charts
        charts_layout = QGridLayout()
        layout.addLayout(charts_layout)

        self.pie_canvas = FigureCanvas(Figure())
        charts_layout.addWidget(self.pie_canvas, 0, 0)

        self.bar_canvas = FigureCanvas(Figure())
        charts_layout.addWidget(self.bar_canvas, 0, 1)

        self.line_canvas = FigureCanvas(Figure())
        charts_layout.addWidget(self.line_canvas, 1, 0)

        self.heatmap_canvas = FigureCanvas(Figure())
        charts_layout.addWidget(self.heatmap_canvas, 1, 1)

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
            ax.pie(cat_stock.values(), labels=cat_stock.keys(), autopct='%1.1f%%')
        ax.set_title("Stock par catégorie")
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
        ax.bar(colors, qtys)
        ax.set_title("Stock par couleur (top 10)")
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
            ax.plot(dates, totals)
        ax.set_title("Évolution stock")
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
        ax.set_title("Heatmap taille/couleur")
        self.heatmap_canvas.draw()