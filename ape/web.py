from ape.Literal import Literal
from ape.Rule import Rule
from ape.Contrary import Contrary
from ape.Aba import Aba
from ape.Attacks import Attack, SetAttack

import re
from nicegui import ui, events
from typing import List, Dict
import html

def make_graph_attacks(aba: Aba):
    """
    Génère un graph des attaques de base
    """
    if aba is None:
        return
    graph:str = "graph TD\n"
    norm_att:set = aba.attacks
    arg:Attack
    for arg in norm_att:
        graph += f"{arg.attacker.name} ==> {arg.attacked.name}\n"

    ui.html("Graphique des attaques")
    ui.mermaid(content=graph, config={'theme': 'default'})

def parse_aba(text: str) -> Aba:
    """
    Parse un texte ABA et retourne un objet Aba.
    """
    print(text)
    aba = Aba()
    # Remove potential \r
    language_re = re.search(r"L: \[(.+?)\]", text)
    assumptions_re = re.search(r"A: \[(.+?)\]", text)
    print(f'ass {assumptions_re}')
    contraries_re = re.findall(r"C\((.+?)\): (.+)", text)
    print(f'cont {contraries_re}')
    contraries_re = [(con[0], con[1].replace('\r', '')) for con in contraries_re]
    print(f'cont {contraries_re}')
    rules_re = re.findall(r"\[(r\d+)\]: (.+?) <- (.*)", text)
    
    rules_re = [(rule[0], rule[1].replace('\r', ''), rule[2].replace('\r', '')) for rule in rules_re]
    print(rules_re)
    pref_re = re.findall(r"PREF: (.+)", text)

    # Parse language
    if language_re:
        literals = [Literal(lit.strip()) for lit in language_re.group(1).split(',')]
        for lit in literals:
            aba.add_literal(lit)

    # Parse assumptions
    if assumptions_re:
        assumptions = [Literal(lit.strip()) for lit in assumptions_re.group(1).split(',')]
        for assumption in assumptions:
            aba.add_assumption(assumption)

    # Parse contraries
    for contrary in contraries_re:
        contrary_obj = Contrary(Literal(contrary[0]), Literal(contrary[1]))
        aba.add_contrary(contrary_obj)
    
    # Parse rules
    for rule in rules_re:
        head = Literal(rule[1].strip())
        if rule[2]:
            body = {Literal(lit.strip()) for lit in rule[2].split(',')}
        else:
            body = set()
        rule_obj = Rule(head, body)
        aba.add_rule(rule_obj)

    # Parse preferences
    preferences: Dict[Literal, set] = {}
    if pref_re:
        pref_string = pref_re[0]
        # Split preference levels by '>'
        levels = [level.strip() for level in pref_string.split('>')]
        # Loop through each level and map preferences
        for i in range(len(levels) - 1):
            higher_literals = [Literal(lit.strip()) for lit in levels[i].split(',')]
            lower_literals = [Literal(lit.strip()) for lit in levels[i + 1].split(',')]
            for higher in higher_literals:
                if higher not in preferences:
                    preferences[higher] = set()
                preferences[higher].update(lower_literals)

    # Add preferences to the ABA object (assuming you have a method for this)
    for higher, lowers in preferences.items():
        for lower in lowers:
            aba.add_preference(higher, lower)
    aba.generate_arguments()
    # print('arg')
    # print(aba)
    aba.generate_attacks()
    # print('att')
    # print(aba)
    aba.computing_normal_and_reverse_attack()
    print('norm')
    print(aba)
    return aba

def exemple_rule():
    """
    Generate exemples
    """
    def create_td4_1():
        """
        From TD4
        """
        a, b, c, q, p, r, s, t = [Literal(x) for x in "abcqprst"]
        return Aba(
            language={a, b, c, q, p, r, s, t},
            rules={Rule(p, {q, a}), Rule(q, set()), Rule(r, {b, c}), Rule(t, {p, c}), Rule(s, {t})},
            assumptions={a, b, c},
            contraries={Contrary(a, r), Contrary(b, s), Contrary(c, t)}
        )

    def create_cour_1():
        """
        From cour
        """
        a, b, c, q, p, r, s, t = [Literal(x) for x in "abcqprst"]
        return Aba(
            language={a, b, c, q, p, r, s, t},
            rules={Rule(p, {q, a}), Rule(q, set()), Rule(r, {b, c})},
            assumptions={a, b, c},
            contraries={Contrary(a, r), Contrary(b, s), Contrary(c, t)}
        )

    examples = {
        "Exemple du TD": create_td4_1(),
        "Exemple du Cour": create_cour_1()
    }

    def reset_page():
        """
        Reset page exemple
        """
        results.clear()
        with results:
            ui.label('Sélectionnez un exemple pour afficher les résultats.').classes('text-h6')

    def load_example(example_name):
        """
        IHM to load exemple
        """
        results.clear()
        aba = examples[example_name]
        aba.generate_arguments()
        aba.generate_attacks()
        with results:
            ui.label(f"Exemple: {example_name}").classes('text-h6')
            ui.label("Framework ABA:").classes('text-bold')
            # Take all space in width
            with ui.scroll_area().classes('w-100 h-100'):
                ui.html(f'<pre>{html.escape(str(aba))}</pre>').classes('font-mono text-sm')
            ui.label(f"Nombre d'arguments générés: {len(aba.arguments)}").classes('text-bold')
            with ui.expansion('Arguments générés', icon='description'):
                for arg in aba.arguments:
                    ui.label(str(arg))
            ui.label(f"Nombre d'attaques générées: {len(aba.attacks)}").classes('text-bold')
            with ui.expansion('Attaques générées', icon='description'):
                for attack in aba.attacks:
                    ui.label(str(attack))
            make_graph_attacks(aba)

    # Interface utilisateur
    with ui.card().classes('w-full'):
        ui.label('ABA Framework - Résultats').classes('text-h5')
        with ui.row():
            for example_name in examples:
                ui.button(example_name, on_click=lambda _, name=example_name: load_example(name))
            ui.button('Réinitialiser', on_click=reset_page).classes('bg-red-500 text-white')
        results = ui.column().classes('w-full')
    reset_page()

def handle_file_upload(e: events.UploadEventArguments):
    """
    Action for upload file
    """
    graph_compenent.clear()
    with graph_compenent:
        ui.label("Graphique des attaques").classes('text-h5')
    file = e.content
    text = file.read().decode('utf-8')
    aba = parse_aba(text)
    display_aba(aba)

def handle_text_submit():
    """
    Action for submit text
    """
    graph_compenent.clear()
    with graph_compenent:
        ui.label("Graphique des attaques").classes('text-h5')
    text = textarea.value
    aba = parse_aba(text)
    display_aba(aba)

def display_aba(aba: Aba):
    """
    IHM to display aba
    """
    aba_output.clear()
    with aba_output:
        ui.label("Framework ABA:").classes('text-bold')
        with ui.scroll_area().classes('w-100 h-100'):
            ui.html(f'<pre>{html.escape(str(aba))}</pre>').classes('font-mono text-sm')
        ui.label(f"Nombre d'arguments générés: {len(aba.arguments)}").classes('text-bold')
        with ui.expansion('Arguments générés', icon='description'):
            for arg in aba.arguments:
                ui.label(str(arg))
        ui.label(f"Nombre d'attaques générées: {len(aba.attacks)}").classes('text-bold')
        with ui.expansion('Attaques générées', icon='description'):
            for attack in aba.attacks:
                ui.label(str(attack))
        ui.label(f"Nombre d'attaques normal générés: {len(aba.normal_attacks)}").classes('text-bold')
        with ui.expansion('Attaques normal', icon='description'):
            for norm_attack in aba.normal_attacks:
                ui.label(str(norm_attack))
            # map(lambda norm_attack: ui.label(str(norm_attack)), aba.normal_attacks)
        ui.label(f"Nombre d'attaques reverse générés: {len(aba.reverse_attacks)}").classes('text-bold')
        with ui.expansion('Attaques reverse', icon='description'):
            for reverse_attack in aba.reverse_attacks:
                ui.label(str(reverse_attack))
            # map(lambda reverse_attack: ui.label(str(reverse_attack)), aba.reverse_attacks)
        make_graph_attacks_norm_reverse(aba)

def make_graph_attacks_norm_reverse(aba: Aba):
    """
    Génère un graph des attaques
    """
    if aba is None:
        return
    graph:str = "graph TD\n"
    norm_att:set = set(aba.normal_attacks)
    reverse_att:set = set(aba.reverse_attacks)
    arg:SetAttack
    for arg in norm_att.intersection(reverse_att):
        graph += f"{'_'.join(map(str, arg.attacker))} ==> {'_'.join(map(str, arg.attacked))}\n"

    for arg in norm_att.difference(reverse_att):
        graph += f"{'_'.join(map(str, arg.attacker))} --> {'_'.join(map(str, arg.attacked))}\n"

    for arg in reverse_att.difference(norm_att):
        graph += f"{'_'.join(map(str, arg.attacker))} -.-> {'_'.join(map(str, arg.attacked))}\n"

    graph += """
subgraph Legend
direction TB
X ==>|reverse and normal attacks| Y
X -->|normal attack| Y
X -.->|revers attack| Y
end
"""
    with graph_compenent:
        ui.mermaid(content=graph, config={'theme': 'default'}).classes('w-full h-full')

    # Add a download button for the PNG image
    # X
def importation():
    global textarea
    global graph_compenent
    global aba_output
    
    with ui.column().classes('w-full'):
        with ui.card():
            ui.label("Importer un fichier ou saisir du texte").classes('text-h5')
            with ui.row(align_items='stretch').classes('w-full'):
                with ui.card():
                    textarea = ui.textarea(placeholder="Collez ici votre texte ABA").classes('w-full h-32')
                    ui.button("Soumettre le texte", on_click=handle_text_submit).classes('bg-blue-500 text-white')
                with ui.card():
                    ui.upload(on_upload=handle_file_upload, label='Importer un fichier texte ABA')
        with ui.row().classes('w-full'):
            graph_compenent = ui.card().classes('w-1/2 h-full')
            with graph_compenent:
                ui.label("Graphique des attaques").classes('text-h5')
            aba_output = ui.column().classes('w-1/3 h-1000')

with ui.tabs().classes('w-full') as tabs:
    tab_exemple = ui.tab('Exemple !')
    tab_importation = ui.tab('Vos importations')

with ui.tab_panels(tabs, value=tab_exemple).classes('w-full'):
    with ui.tab_panel(tab_exemple):
        exemple_rule()
    with ui.tab_panel(tab_importation):
        importation()

ui.run(title="ABA Framework")
