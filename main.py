from pathlib import Path
from bs4 import BeautifulSoup
import re
import ngram_toolkit as ngtk

html_path = Path(Path.cwd(), 'data/leaderTalk.html')
# The following question can be changed to extract the answers for any of the available questions in the webpage tables
sel_ques = 'what is your favorite thing about cognizant?'          # Must be all lowercase
consolidated = ''

soup = BeautifulSoup(open(html_path, encoding='utf-8'), 'html.parser')

fdist_list = [None, None, None, None]


def clean_text(inp_text, lower = False):
    """
    Convert multi-line text to single line, clean up multi-spaces and trailing/leading blankspaces
    :param inp_text: The original text
    :param lower: Returns all lowercase text if True, otherwise unchanged
    :return: Beautiful text
    """
    out_text = inp_text.replace('\n', ' ').strip()
    out_text = re.sub(r'\s+', ' ', out_text)
    if lower:
        out_text = out_text.lower()
    return out_text


for summary in soup.findAll('div', {'class': 'video-summary-wrap'}):
    table = summary.find('table')
    for tr in table.find_all('tr'):
        sel_ques_flag = False
        for td in tr.find_all('td'):
            if sel_ques_flag:
                consolidated += clean_text(td.find('p').text)
                break
            if clean_text(td.find('p').text, lower=True) == sel_ques:
                sel_ques_flag = True

full_ngram = ngtk.Ngram(consolidated)
words = ''
for i in range(3):
    fdist_list[i] = full_ngram.get_fdist(i + 1)
    # Keep only the ngrams which have frequency more than 1
    non_unique = list(filter(lambda x: x[1] > 1, fdist_list[i].items()))

    for tpl in non_unique:
        if i == 0:
            words = words + ' ' + ' '.join([tpl[0]] * tpl[1])
        else:
            words = words + ' ' + ' '.join(['_'.join(tpl[0])] * tpl[1])

ngtk.Ngram.get_word_cloud(words)
