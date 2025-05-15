import pytest
import os
from pta_automation.config.config_parser import ConfigParser
from pta_automation.framework.utilities.common import save_excel

@pytest.mark.pta
class TestPTA:
    """
    Test cases for PTA Application
    """
    def test_excel(self, request):
        """
        Test #01 : Read the data from Excel file and write results to a new output file.
        """
        sheet_name = 'PTA'
        config_name = 'ui_test_excel_data_config'
        # Step 1: Load the Excel data
        df = ConfigParser.load_xlsx(config_name, sheet_name)
        print("Original Data:\n", df)

        # Step 2: Process rows and update status
        for idx, row in df.iterrows():
            if row.get('Run') == 'Y':
                test_case = row.get('Tets Case')
                username = row.get('UserName')
                password = row.get('Password')

                print(f"Running Test Case: {test_case} with User: {username}")

                # Dummy test logic - mark Pass
                df["Status"] = df["Status"].astype(str)  # Ensure it's string-compatible
                df.at[idx, 'Status'] = 'Pass'

        # Step 3: Copy original Excel file to output version
        input_path = ConfigParser.resolve_config_path("ui_test_excel_data_config")
        base, ext = os.path.splitext(input_path)
        output_path = base + '_output' + ext

        save_excel(sheet_name, df, input_path, output_path)

        print(f"\nUpdated Excel written to: {output_path}")