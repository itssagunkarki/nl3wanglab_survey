import pandas as pd
import datetime
import os


class SurveyQuestion:
    def __init__(self, number: int, prompt: str, reverse: int, category: str, response: int):
        self.number = number
        self.prompt = prompt
        self.reverse = reverse
        self.category = category
        self.response = response

    def __str__(self):
        return self.prompt

    def get_question_number(self):
        return self.number

    def get_question_prompt(self):
        return self.prompt

    def get_question_reverse(self):
        return self.reverse

    def get_question_category(self):
        return self.category

    def set_response(self, response):
        self.response = response

    def get_response(self):
        return self.response


class SurveyDetails:
    def __init__(self, survey_id: str, data_entered_by: str, first_data_entry_date: datetime, verifying_data_entry_date: datetime, first_data_is_equals_to_second_entry: bool):
        self.survey_id = survey_id
        self.data_entered_by = data_entered_by
        self.first_data_entry_date = first_data_entry_date
        self.verifying_data_entry_date = verifying_data_entry_date
        self.first_data_is_equals_to_second_entry = first_data_is_equals_to_second_entry

    def set_survey_id(self, survey_id):
        self.survey_id = survey_id

    def set_data_entered_by(self, data_entered_by):
        self.data_entered_by = data_entered_by

    def set_first_data_entry_date(self, first_data_entry_date):
        self.first_data_entry_date = first_data_entry_date

    def set_verifying_data_entry_date(self, verifying_data_entry_date):
        self.verifying_data_entry_date = verifying_data_entry_date

    def set_first_data_is_equals_to_second_entry(self, first_data_is_equals_to_second_entry):
        self.first_data_is_equals_to_second_entry = first_data_is_equals_to_second_entry


class Questions:
    def __init__(self, questions: dict):
        self.questions = questions

    def get_questions(self):
        return self.questions

    def dict_to_dataframe(self):
        # Convert the dictionary to a list of dictionaries
        survey_questions_list = []
        for key, value in self.questions.items():
            survey_questions_list.append({
                'cbq_num': value.number,
                'cbq_q': value.prompt,
                'reverse': value.reverse,
                'cbq_scale_cat': value.category,
                'cbq_a': value.response
            })

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(survey_questions_list)
        return df


class QuestionFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.excel_file = pd.ExcelFile(self.file_path)
        self.details_df = pd.read_excel(self.excel_file, sheet_name='details')
        self.questions_df = pd.read_excel(
            self.excel_file, sheet_name='questions')

    def _clean_question_df(self):
        self.questions_df.fillna(0, inplace=True)
        self.questions_df['reverse'] = (self.questions_df['reverse'] == "R")
        self.questions_df.dtypes

        self.questions_df['cbq_scale_cat'] = self.questions_df['cbq_scale_cat'].astype(
            str)
        self.questions_df['cbq_q'] = self.questions_df['cbq_q'].astype(str)
        self.questions_df['cbq_num'] = self.questions_df['cbq_num'].astype(int)
        self.questions_df['reverse'] = self.questions_df['reverse'].astype(
            bool)
        self.questions_df['cbq_a'] = self.questions_df['cbq_a'].astype(int)

        self.questions_df.sort_values(by=['cbq_num'], inplace=True)

    def _question_row_to_object(self, row):
        return SurveyQuestion(
            number=row['cbq_num'],
            prompt=row['cbq_q'],
            reverse=row['reverse'],
            category=row['cbq_scale_cat'],
            response=row['cbq_a']
        )

    def get_questions_as_dict(self):
        self._clean_question_df()
        questions = {}
        for index, row in self.questions_df.iterrows():
            question = self._question_row_to_object(row)
            questions[question.get_question_number()] = question
        
        return Questions(questions)
