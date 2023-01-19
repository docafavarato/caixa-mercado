from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from products import products_dict
from discounts import discounts_dict
from winsound import Beep
from datetime import datetime
import sys
import webbrowser
import a_rc

listed_products = {}
final_price = 0
nfe = []
discounts = []

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('ui/main.ui', self)
        
        self.nfe = NfeWindow()
        self.nfe_button.clicked.connect(self.nfe.show)
        self.nfe_button.clicked.connect(self.nfe.register)
        
        self.register_button.clicked.connect(self.register)
        self.discount_button.clicked.connect(self.give_discount)
        self.remove_button.clicked.connect(self.remove)
        self.github.clicked.connect(self.open_github)
        self.clear.clicked.connect(self.clear_products_list)
    
        self.show()
        
    def register(self):
        global final_price
        total = self.total
        product_name = self.product_name
        product_qtd = self.product_qtd
        code = self.save_product.text().upper()
        amount = self.product_amount.value()
        products_list = self.products_list
        products_price = self.products_list2
        
        try:
            if amount > 1:
                products_list.addItem(products_dict[code][0])
                products_price.addItem('R$'+str(products_dict[code][1])+f'       x{amount}')
                product_name.setText(f'{products_dict[code][0]}')
                product_qtd.setText(f'x{amount}')
                listed_products[products_dict[code][0]] = [products_dict[code][1], amount]
                final_price += products_dict[code][1] * amount
                nfe.append((products_dict[code][0], products_dict[code][1]))
                total.setText('Total: {:.2f}'.format(final_price))
                Beep(900,50)
            
            else:
                products_list.addItem(products_dict[code][0])
                products_price.addItem('R$'+str(products_dict[code][1])+f'       x{amount}')
                product_name.setText(f'{products_dict[code][0]}')
                product_qtd.setText(f'x{amount}')
                listed_products[products_dict[code][0]] = [products_dict[code][1], amount]
                final_price += products_dict[code][1]
                nfe.append((products_dict[code][0], products_dict[code][1]))
                total.setText('Total: {:.2f}'.format(final_price))
                Beep(900,50)
                
            self.product_amount.setValue(1)
            
        except KeyError:
            product_name.setText(f'O produto {code} não foi encontrado.')
        
        self.save_product.clear()
        
    def give_discount(self):
        global final_price
        code = self.discount_input.text().upper()
        if len(discounts) < 1:
            if code in discounts_dict:
                self.total.setText('Total: {:.2f}'.format(final_price*discounts_dict[code]))
                final_price = final_price*discounts_dict[code]
                discounts.append(1)
            else:
                self.product_name.setText(f'O cupom {code} não existe')
        else:
            self.product_name.setText('Só é permitido a utilização de um cupom por vez.')
        self.discount_input.clear()
        
    def on_change(self):
        return [item.text() for item in self.products_list.selectedItems()]
    
    def multiplier_on_change(self):
        return [item.text() for item in self.products_list2.selectedItems()]
    
    def remove(self):
        global final_price
        items = Ui.on_change(self)
        try:
            for item in items:
                row = self.products_list.currentRow()
                if row == 0:
                    multiplier = int(self.products_list2.item(0).text().split('x')[1])
                else:
                    multiplier = int(self.products_list2.item(self.products_list.currentRow()).text().split('x')[1])

                self.products_list.takeItem(row)
                self.products_list2.takeItem(row)
                listed_products.pop(item)
                for key in products_dict:
                    if item in products_dict[key][0]:
                        final_price -= (products_dict[key][1]*multiplier)
                        self.total.setText('Total: {:.2f}'.format(final_price))
                        
        except IndexError:
            self.product_name.setText('Não existe nenhum produto registrado no momento.')
    
    def open_github(self):
        webbrowser.open('https://github.com/docafavarato/')
        
    def clear_products_list(self):
        global final_price
        global listed_products
        q = QMessageBox.question(self, 'Limpar o carrinho', "Deseja limpar o carrinho?", QMessageBox.Yes | QMessageBox.No)
        if q == QMessageBox.Yes:
            self.products_list.clear()
            self.products_list2.clear()
            listed_products.clear()
            final_price = 0
            self.total.setText('Total: {:.2f}'.format(final_price))
            self.product_name.setText('')
            self.product_qtd.setText('')
        else:
            pass
        
class NfeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(NfeWindow, self).__init__()
        uic.loadUi('ui/nfe.ui', self)
        
    def register(self):
        now = datetime.now()
        self.header.setText(now.strftime('%d/%m/%Y %H:%M:%S'))
        
        for i in listed_products:
            print(i)
            self.listWidget.addItem(f'{i} - {listed_products[i][0]} x{listed_products[i][1]}')
            self.listWidget.addItem('-'*60)
       
        self.listWidget.addItem('Total: {:.2f}'.format(final_price))
    
    def closeEvent(self, event):
        self.listWidget.clear()
        event.accept()
        
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()