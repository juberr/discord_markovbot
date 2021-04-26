def parse_jep(jep):
    
    def answer_cleaner(string):
        
        string = string.lower()
        
        if '<i>' in string:
            string = string[3:-4]
            
        articles = ['the', 'a']
        
        if string.split(' ')[0] in articles:
            
            words = string.split(' ')[1:]
            string = ' '.join(words)
            
        if '&' in string:
            string = string.replace('&','and')
            
        
        return string
    
    question = jep[0]['question']
    
    value = jep[0]['value']
    
    category = jep[0]['category']['title'].title()
    
    answer = answer_cleaner(jep[0]['answer'])
    
    return question, value, category, answer

def clean_answer(answer):

    if answer.split()[2] in ['a', 'the']:
        answer = answer.split()[3:]

        return ' '.join(answer)
    
    else: return ' '.join(answer.split()[2:])
    
