import json
from core.inventory import Inventory
from core.supplier import Supplier
from core.purchase_order import PurchaseOrder
from tools.whatsapp_notifier import WhatsAppNotifier
from utils.nlp import understand_query

class SupplyChainAgent:
    def __init__(self):
        self.inventory = Inventory()
        self.supplier = Supplier()
        self.purchase_order = PurchaseOrder()
        self.notifier = WhatsAppNotifier()

    def process_query(self, query):
        """Processes the user's query and takes action."""
        parsed_query_str = understand_query(query)
        # Clean the string to be valid JSON
        parsed_query_str = parsed_query_str.strip().replace("`", "")
        if parsed_query_str.startswith("json"):
            parsed_query_str = parsed_query_str[4:]

        try:
            parsed_query = json.loads(parsed_query_str)
        except json.JSONDecodeError:
            return "Sorry, I couldn't understand that. Could you rephrase?"

        intent = parsed_query.get("intent")
        entities = parsed_query.get("entities", {})

        if intent == "check_stock":
            item = entities.get("item_name")
            return self.inventory.check_stock(item)

        elif intent == "update_stock":
            item = entities.get("item_name")
            quantity_to_add = int(entities.get("quantity", "0"))
            return self.inventory.update_stock(item, quantity_to_add)

        elif intent == "predict_shortage":
            return self.inventory.predict_shortage()

        elif intent == "create_po":
            item = entities.get("item_name")
            quantity_str = entities.get("quantity", "0")
            quantity = int("".join(filter(str.isdigit, quantity_str)))
            unit = "".join(filter(str.isalpha, quantity_str))
            supplier_name = entities.get("supplier")
            price = entities.get("price", "30") # Default price for now

            if not supplier_name:
                supplier_name = self.supplier.find_supplier_for_item(item)

            po_text, po_id = self.purchase_order.create_po_text(item, quantity, unit, price, supplier_name)
            pdf_file = self.purchase_order.create_po_pdf(po_text, po_id)

            # In a real app, you'd get the supplier's number from the sheet
            supplier_whatsapp = "+919876543210" # Mock number
            self.notifier.send_pdf(supplier_whatsapp, pdf_file, f"New PO: {po_id}")

            return f"Purchase order {po_id} created and sent to {supplier_name}."

        else:
            return "Sorry, I'm not sure how to handle that."