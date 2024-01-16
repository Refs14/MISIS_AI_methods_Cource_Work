from rasa_sdk          import Action, Tracker
from rasa_sdk.events   import SlotSet
from rasa_sdk.executor import CollectingDispatcher
 
from datetime import datetime as dt
from typing import Any, Text, Dict, List
from difflib import SequenceMatcher
import io


from qiskit import QuantumCircuit


class ActionChooseOption(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_choose_option"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(buttons = [
                {"payload": "/get_gate_by_name", "title": "Получить гейт по названию"},
                {"payload": "/calculate", "title": "Произвести расчет"},
                {"payload": "/create_circuit", "title": "Создать схему из N кубитов"},
                {"payload": "/request_circuit", "title": "Вывести схему"}
            ])

        return []
    
class ActionPrintCircuit(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_print_circuit"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        string = tracker.get_slot("CIRCUIT")
        dispatcher.utter_message(str(QuantumCircuit().from_qasm_str(string).draw("text")))
        return []

class ActionCreateCircuit(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_create_circuit"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        qubit_number = int(tracker.get_slot("NUMBER"))
        circuit = QuantumCircuit(qubit_number)
        dispatcher.utter_message(f'Circuit with {qubit_number} qubits created')
        dispatcher.utter_message(str(circuit.draw("text")))

        return [SlotSet("CIRCUIT", circuit.qasm())]
    

class ActionGetGateInfo(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_get_gate_info"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        gate_number = int(tracker.get_slot("NUMBER"))
        dispatcher.utter_message(f'Gate {gates_info[gate_number-1][0]}')
        for row in gates_info[gate_number-1][1]:
            dispatcher.utter_message(f'{row}')
        return []
    
class ActionCalculate(Action):
 
    def name(self) -> Text:              # регистрируем имя действия
        return "action_calculate"
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        circuit = QuantumCircuit().from_qasm_str(tracker.get_slot("CIRCUIT"))
        gate_input = tracker.latest_message['text']
        gate_name = gate_input.split('(')[0]
        if(gate_name == "x"):
            circuit.x(int(gate_input[2]))
        elif(gate_name == "y"):
            circuit.y(int(gate_input[2]))
        elif(gate_name == "z"):
            circuit.z(int(gate_input[2]))
        elif(gate_name == "s"):
            circuit.s(int(gate_input[2]))
        elif(gate_name == "h"):
            circuit.h(int(gate_input[2]))
        elif(gate_name == "cx"):
            circuit.cx(int(gate_input[3]), int(gate_input[-2]))
        elif(gate_name == "cz"):
            circuit.cz(int(gate_input[3]), int(gate_input[-2]))
        elif(gate_name == "swap"):
            circuit.swap(int(gate_input[5]), int(gate_input[-2]))

        dispatcher.utter_message(f'gate: {gate_input}')
        dispatcher.utter_message(str(circuit.draw("text")))

        return [SlotSet("CIRCUIT", circuit.qasm())]
    



# x y z h s cx cz swap
gates_info = []
gates_info.append(["x", [[0, 1], 
                         [1, 0]]])

gates_info.append(["y", [[0, complex(0, -1)], 
                         [complex(0, 1), 0]]])

gates_info.append(["z", [[1, 0], 
                         [0, -1]]])

rev_sqrt2 = round((1/2)**0.5, 3)
gates_info.append(["h", [[rev_sqrt2, rev_sqrt2], 
                         [rev_sqrt2, -rev_sqrt2]]])

gates_info.append(["s", [[1, 0], 
                         [0, complex(0, 1)]]])

gates_info.append(["cx", [[1, 0, 0, 0], 
                         [0, 1, 0, 0], 
                         [0, 0, 0, 1], 
                         [0, 0, 1, 0]]])

gates_info.append(["cz", [[1, 0, 0, 0], 
                         [0, 1, 0, 0], 
                         [0, 0, 1, 0], 
                         [0, 0, 0, -1]]])

gates_info.append(["swap", [[1, 0, 0, 0], 
                         [0, 0, 1, 0], 
                         [0, 1, 0, 0], 
                         [0, 0, 0, 1]]])
