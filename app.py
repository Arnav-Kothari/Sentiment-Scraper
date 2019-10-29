
def store_data(infile, file_data):

	for word in f.read().split():
		file_data.append(word)

def check_sym(file_data, curr_word):
    x = len(curr_word) - 1;
    sym = curr_word[x]
    if sym == '?' or sym == '!':
        return 1;
    return 0;

f = open("text.txt", "r")
file_data = []
store_data(f, file_data)
print(file_data)
sym_count = 0
for word in file_data:
    if check_sym(file_data, word):
        sym_count = sym_count + 1
print(sym_count)
f.close()



