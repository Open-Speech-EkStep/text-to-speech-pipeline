from filter import DataFilter

input_arr_sc = ['ज़यादातर 1234        कैसे-कैसे १२३४ सुझाव देने वाले लोग वो हैं, मुझ! abcd तक पहुँचने का प्रयास करने वाले लोग वो हैं, ']

obj = DataFilter("hi",  '[^ ँ-नप-रल-ळव-ह़-्ॐॠ-ॡ।-॰]+')
data = obj.filter_data(input_arr_sc)

print(data)