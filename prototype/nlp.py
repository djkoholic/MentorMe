import pandas as pd

def convert_to_df(mentors):
    mentors = [mentor.__dict__ for mentor in mentors]
    mentors_df = pd.DataFrame.from_records(mentors)
    mentors_df = mentors_df.drop(['_state', 'last_login', 'user_type', 'password', 'is_admin', 'is_staff', 'is_active', 'is_superuser'], axis=1)
    return mentors_df.head()