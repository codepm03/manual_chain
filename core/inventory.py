import gspread
from google.oauth2.service_account import Credentials

class Inventory:
    def __init__(self):
        # Authenticate with Google Sheets
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open("inventory").worksheet("Inventory_supply")

    def check_stock(self, item_name):
        """Checks the stock level of a given item."""
        # This is a placeholder implementation.
        # In a real application, this would search the Google Sheet for the item.
        return f"Stock for {item_name} is 50 units."

    def predict_shortage(self):
        """Predicts potential stock shortages."""
        # This is a placeholder implementation.
        return "No shortages predicted."

    def update_stock(self, item_name, quantity_to_add):
        """Updates the stock level of a given item."""
        try:
            cell = self.sheet.find(item_name)
            current_quantity = int(self.sheet.cell(cell.row, cell.col + 1).value)
            new_quantity = current_quantity + quantity_to_add
            self.sheet.update_cell(cell.row, cell.col + 1, new_quantity)
            return f"Stock for {item_name} updated to {new_quantity}."
        except gspread.exceptions.CellNotFound:
            return f"Item '{item_name}' not found in inventory."
        except Exception as e:
            return f"An error occurred: {e}"
