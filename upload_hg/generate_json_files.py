import sys

import pandas as pd

sys.path.append("./src")


def main():
    from modelset import load
    for model_type in ['ecore', 'uml']:
        dataset = load(modeltype=model_type, selected_analysis=['stats'])
        dataset_df = dataset.to_normalized_df(min_occurrences_per_category=10)
        dataset_df_no_dups = dataset.to_normalized_df(remove_duplicates=True,
                                                      min_occurrences_per_category=10)

        ids = list(dataset_df['id'])
        ids_no_dups = list(dataset_df_no_dups['id'])
        print(f'Full dataset {len(ids)}')
        print(f'No dup dataset {len(ids_no_dups)}')
        labels = list(dataset_df['category'])

        txt_filenames = [dataset.txt_file(i) for i in ids]
        txt_contents = []
        for f in txt_filenames:
            with open(f, 'r') as file:
                data = file.read()
                txt_contents.append(data)

        graph_filenames = [dataset.graph_file(i) for i in ids]
        graph_contents = []
        for f in graph_filenames:
            with open(f, 'r') as file:
                data = file.read()
                graph_contents.append(data)

        # Important: Actually, if True, the model does not belong in the deduplicated version
        is_dup = [True if i not in ids_no_dups else False for i in ids]
        print(f'Duplicate: {len([f for f in is_dup if f==True])}')
        print(f'No Duplicate: {len([f for f in is_dup if f == False])}')

        # XMI
        xmi_files = [dataset.model_file(dataset.get_model_by_id(i)) for i in ids]
        xmi_contents = []
        for f in xmi_files:
            with open(f, 'r') as file:
                data = file.read()
                xmi_contents.append(data)

        final_pd = pd.DataFrame.from_dict({
            "ids": ids,
            "labels": labels,
            "txt": txt_contents,
            "graph": graph_contents,
            "xmi": xmi_contents,
            "model_type": [model_type for _ in range(len(ids))],
            "is_duplicated": is_dup
        })

        final_pd.to_json(f'{model_type}.jsonl', orient='records')


if __name__ == '__main__':
    main()
