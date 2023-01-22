from datasets import load_dataset
import json

dataset_hg = load_dataset('antolin/modelset', split="train")

print(dataset_hg)
print(dataset_hg["xmi"][0])
