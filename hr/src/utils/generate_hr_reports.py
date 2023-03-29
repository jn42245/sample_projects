# Created on 2 Dec 2022
# Author: Thierry Tran
# Script to generate word compensation letters from raw Excel file

import os
import re
import calendar
import pandas as pd
from pathlib import Path
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
from datetime import datetime

# Internal module
from dataload.json_objects import load_json
from utils.plotly_graphs import pie_chart


def run_report(path_raw_data: Path, path_template: Path, path_output: Path, year_input: int):

    # Create required variables
    current_dir = os.path.dirname(os.path.abspath("__file__"))
    date_str = datetime.today().strftime('%Y%m%d')
    sqt_colours = load_json(os.path.join(current_dir, 'data', 'sqt_colours.json'), "r")

    # Load raw data
    raw_data = pd.read_excel(path_raw_data, sheet_name='raw',
                             converters={'base_salary': int, 'sal_increase': int}).to_dict()
    hr_context = pd.read_excel(path_raw_data, sheet_name='hr').to_dict('records')

    # Create context and output to word document
    for ix in range(0, len(raw_data['name'])):
        context = {}
        for key in raw_data:
            context[key] = raw_data[key][ix]

        # Update context with additional elements
        word_template = DocxTemplate(path_template)
        context['year'] = year_input
        context['year_1'] = year_input + 1
        context['pc_increase'] = (context['sal_increase'] - context['base_salary']) / context['base_salary'] * 100
        context['date_effect'] = '{d} {m} {y}'.format(d=context['date_effect'].date().day,
                                                      m=calendar.month_name[context['date_effect'].date().month],
                                                      y=context['date_effect'].date().year)
        context['pc_pension'] = context['pc_pension'] * 100
        context['allowances'] = sum((context['fitness_allowance'], context['wellness_allowance'],
                                     context['learning_allowance'], context['shelter_allowance'],
                                     context['shelter_allowance'], context['vol_allowance'],
                                     context['community_allowance']))
        context['benefits'] = int(context['pc_pension'] / 100 * context['base_salary'])
        context['total_salary'] = sum(
            (context['base_salary'], context['bonuses'], context['benefits'], context['allowances']))
        context.update(hr_context[0])

        # Plotly graphs
        labels = ['Base Salary', 'Bonuses', 'Benefits', 'Allowances']
        values = [context['base_salary'], context['bonuses'], context['benefits'], context['allowances']]
        marker_colors = [sqt_colours['allstate_navy'], sqt_colours['allstate_light_blue'], sqt_colours['allstate_blue'],
                         sqt_colours['accent_coral']]

        fig = pie_chart(labels, values, marker_colors, 1500, 1000)
        fig.write_image(os.path.join(path_output, 'temp.jpeg'))
        context['graph_salary'] = InlineImage(word_template, os.path.join(path_output, 'temp.jpeg'), Cm(10))

        # Add comma to numbers
        for item in ('base_salary', 'sal_increase', 'bonuses', 'fitness_allowance',
                     'wellness_allowance', 'learning_allowance', 'shelter_allowance',
                     'vol_allowance', 'community_allowance', 'allowances', 'benefits', 'total_salary'):
            context[item] = '{:,}'.format(context[item])

        # Output data
        output_name_str = re.sub('[ .]', "", context['name'])
        word_template.render(context)
        word_template.save(os.path.join(path_output, '{d}_{n}.docx'.format(d=date_str, n=output_name_str)))
        os.remove(os.path.join(os.path.join(path_output, 'temp.jpeg')))

        # Convert docx to pdf
        convert(path_output)

    return None


if __name__ == "__main__":

    wk_dir = os.path.dirname(os.path.abspath("__file__"))

    run_report(Path(os.path.join(wk_dir, 'data', 'test_data.xlsx')),
               Path(os.path.join(wk_dir, 'data', 'template.docx')),
               Path(os.path.join(wk_dir, 'Output')),
               2020)
