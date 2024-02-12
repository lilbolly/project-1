from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from datetime import datetime, timedelta

class GestionnaireFinancier:
    def __init__(self, somme_initiale, date_limite):
        self.somme_actuelle = somme_initiale
        self.somme_jour = 0
        self.date_limite = date_limite

    def calculer_somme_quotidienne(self):
        jours_restants = (self.date_limite - datetime.today().date()).days
        return round((self.somme_actuelle) / jours_restants, 2)

    def depenser(self, montant):
        somme_quotidienne = self.calculer_somme_quotidienne()
        if montant <= somme_quotidienne:
            self.somme_jour += montant
            return True
        else:
            return False

    def redistribuer_argent_journalier(self):
        somme_quotidienne = self.calculer_somme_quotidienne()
        montant_non_depense = somme_quotidienne - self.somme_jour
        self.somme_actuelle += montant_non_depense
        self.somme_jour = 0

    def redéfinir_somme_date(self, nouvelle_somme, nouvelle_date):
        self.somme_actuelle = nouvelle_somme
        self.date_limite = nouvelle_date

class GestionnaireFinancierApp(App):
    def build(self):
        self.gestionnaire_financier = None

        # Layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Widgets
        layout.add_widget(Label(text="Somme Initiale:"))
        self.somme_initiale_input = TextInput()
        layout.add_widget(self.somme_initiale_input)

        layout.add_widget(Label(text="Date Limite (YYYY-MM-DD):"))
        self.date_limite_input = TextInput()
        layout.add_widget(self.date_limite_input)

        layout.add_widget(Label(text="Montant à Dépenser:"))
        self.montant_depense_input = TextInput()
        layout.add_widget(self.montant_depense_input)

        self.etat_somme_quotidienne_label = Label(text="État Somme Quotidienne:")
        layout.add_widget(self.etat_somme_quotidienne_label)

        layout.add_widget(Button(text="Initialiser", on_press=self.initialiser))
        layout.add_widget(Button(text="Dépenser", on_press=self.depenser))
        layout.add_widget(Button(text="Redistribuer", on_press=self.redistribuer))

        return layout

    def initialiser(self, instance):
        somme_initiale_str = self.somme_initiale_input.text
        date_limite_str = self.date_limite_input.text

        try:
            somme_initiale = float(somme_initiale_str)
            date_limite = datetime.strptime(date_limite_str, "%Y-%m-%d").date()
        except ValueError:
            self.show_error_popup("Erreur", "Veuillez entrer des valeurs valides pour la somme initiale et la date limite.")
            return

        self.gestionnaire_financier = GestionnaireFinancier(somme_initiale, date_limite)
        self.mettre_a_jour_etat_somme_quotidienne()
        self.show_info_popup("Initialisation", "Gestionnaire Financier initialisé avec succès!")

    def depenser(self, instance):
        if self.gestionnaire_financier:
            montant_str = self.montant_depense_input.text

            try:
                montant = float(montant_str)
            except ValueError:
                self.show_error_popup("Erreur", "Montant invalide. Assurez-vous d'entrer un nombre valide.")
                return

            if self.gestionnaire_financier.depenser(montant):
                self.show_info_popup("Dépense", f"{montant} dépensé avec succès!")
                self.mettre_a_jour_etat_somme_quotidienne()
            else:
                self.show_warning_popup("Dépense", "Montant supérieur à la somme quotidienne disponible.")

    def redistribuer(self, instance):
        if self.gestionnaire_financier:
            self.gestionnaire_financier.redistribuer_argent_journalier()
            self.show_info_popup("Redistribution", "Argent journalier redistribué avec succès!")
            self.mettre_a_jour_etat_somme_quotidienne()

    def mettre_a_jour_etat_somme_quotidienne(self):
        if self.gestionnaire_financier:
            somme_quotidienne = self.gestionnaire_financier.calculer_somme_quotidienne()
            somme_depensee = self.gestionnaire_financier.somme_jour
            somme_restante = somme_quotidienne - somme_depensee
            self.etat_somme_quotidienne_label.text = f"Somme Quotidienne: {somme_quotidienne:.2f}, Porte-monnaie: {somme_restante:.2f}"

    def show_info_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size=(400, 200), auto_dismiss=True)
        popup.open()

    def show_warning_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size=(400, 200), auto_dismiss=True)
        popup.open()

    def show_error_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size=(400, 200), auto_dismiss=True)
        popup.open()

if __name__ == "__main__":
    GestionnaireFinancierApp().run()
