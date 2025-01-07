import os
import pandas as pd
# progess bar
import tqdm

def load_data(file_path: str = 'data/kialoPairsEnglist.csv') :

    """
    Load the data from the csv file and return the train, validation and test data loaders.
    shape of the data : 
    ,topic,,argSrc,argTrg, relation
    0,"['Sports', 'USA', 'Football', 'American_Football', 'Entertainment']",The institution of American football alienates many communities.,Football is very popular and a critical part of many communities.,attack
    """
    df = pd.read_csv(file_path, index_col=0)

    # Rename relation column to a label column and convert the relation to a label
    df = df.rename(columns={'relation':'labels'})
    df['labels'] = df['labels'].map({'attack':0, 'support':1})
    
    # Drop the topic column
    # df = df.drop(columns=['topic'])
    df = df[~df["argSrc"].str.contains(r'See \d+(\.\d+)*')]
    df = df.rename(columns={'topic':'topic' ,'argSrc':'text_a', 'argTrg':'text_b'})
    df.columns = ['topic', 'text_a', 'text_b', 'labels']
    
    return df

# parcour data to create literals, and rules

def transitive2(text_a, text_b, data, counter=-1, number_attacks= 0,number_support=0):
    """
    Check if there is a transitive relation between text_a and text_b
    """
    for index, row in data.iterrows():
        if row['text_a'] == text_b:
            if row['text_b'] == text_a:
                if row['labels'] == 0:
                    number_attacks += 1
                return number_attacks
            elif counter == 0:
                return None
            counter -= 1
            if row['labels'] == 0:
                number_attacks += 1
            return transitive2(text_a, row['text_b'], data, counter, number_attacks)
    return None

def find_all_children_number(text_a:str, data:dict, profondeur=1,number_attack=1) -> set:
    data_children = set()
    profondeur -= 1
    for index, row in data.iterrows():
        if row['text_b'] == text_a:
            if row['labels'] == 0:
                new_attack = 1 + number_attack
            else :
                new_attack = number_attack
            # data_children.add(tuple(row['text_a'], number_attack))
            if profondeur < 1:
                data_children.add((row['text_a'], new_attack%2))
            else :
                data_children = data_children.union(find_all_children_number(row['text_a'], data, profondeur, new_attack))
    return data_children


def all_argument_profondeur(data_to_parcour:pd.DataFrame, profondeur=2) -> pd.DataFrame:
    with tqdm.tqdm(total=len(data_to_parcour)) as pbar:
        all_argument = pd.DataFrame()
        for index, row in data_to_parcour.iterrows():
            res:set = find_all_children_number(row['text_a'], data_to_parcour, profondeur)
            for arg, label in res:
                new_row = pd.DataFrame({'text_a': [arg], 'text_b': [row['text_a']], 'labels': [label]})
                all_argument = pd.concat([all_argument, new_row], ignore_index=True)
            pbar.set_description(f"Iteration {index}/{len(data_to_parcour)}")
            pbar.update(1)
    return all_argument



def find_all_distance_dico(data_to_find:dict, profondeur_base=1, number_attacks:int = 1) -> dict:
    """
    Find all the distance between the text_a and text_b in the data
    """
    # Create a new dataframe to store the distance between text_a and text_b
    data_distance = pd.DataFrame(columns=['text_a', 'text_b', 'labels'])
    for text_a, value in data_to_find.items():
        profondeur = profondeur_base
        number_attacks = 1
        target = value['target']
        number_attacks += value['label']
        try:
            while profondeur > 1:
                if target not in data_to_find:
                    assert False
                if data_to_find[target]['label'] == 0:
                    number_attacks += 1
                target =  data_to_find[target]['target']
                profondeur -= 1
            # add text_a, text_b, number_attacks%2 to data_distance
        except AssertionError:
            continue
        data_distance = pd.concat([data_distance, pd.DataFrame({'text_a': [text_a], 'text_b': [target], 'labels': [number_attacks%2]})], ignore_index=True)
        
    return data_distance

data = load_data()
# Df to dict

DEEP = 3

if os.path.exists(f'data/distance{DEEP}.csv'):
    os.remove(f'data/distance{DEEP}.csv')

# separate data in list of df by topic
data_by_topic = {}
for index, row in data.iterrows():
    if row['topic'] in data_by_topic:
        data_by_topic[row['topic']] = pd.concat([data_by_topic[row['topic']], pd.DataFrame(row).T], ignore_index=True)
    else :
        data_by_topic[row['topic']] = pd.DataFrame(row).T

with tqdm.tqdm(total=len(data_by_topic)) as pbar:
    for key, value in data_by_topic.items():
        pbar.set_description(f"Distance {DEEP} topic :  {key}")
        pbar.update(1)
        data_dico = {}
        for index, row in value.iterrows():
            data_dico[row['text_a']] = {
                    'target' :row['text_b'],
                    'label' : row['labels']
            }
        df:pd.DataFrame = find_all_distance_dico(data_dico, DEEP)
        if not df.empty:
            if os.path.exists(f'data/distance{DEEP}.csv'):
                df.to_csv(f'data/distance{DEEP}.csv', mode='a', header=False)
            else :
                df.to_csv(f'data/distance{DEEP}.csv')



# reprend = True

# with tqdm.tqdm(total=len(data_by_topic)) as pbar:
#     for id, topic in data_by_topic.items():
#         pbar.set_description(f"Distance {DEEP} topic :  {id}")
#         pbar.update(1)
#         # if id  == "['Ethics', 'Philosophy', 'LifeAndDeath', 'Religion', 'God', 'Atheism']":
#         #     reprend = False
#         # if reprend:
#         #     continue
#         df = all_argument_profondeur(topic, DEEP)
#         # add df to distance2.csv
#         if not df.empty:
#             if os.path.exists(f'data/distance{DEEP}.csv'):
#                 df.to_csv(f'data/distance{DEEP}.csv', mode='a', header=False)
#             else :
#                 df.to_csv(f'data/distance{DEEP}.csv')
        
