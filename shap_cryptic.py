from utils.shap_cryptic_utils import *
import argparse

parser = argparse.ArgumentParser(description='Linear Reg on Dataset')
parser.add_argument('--npz_file', default='./extracted_data/VARIANTS_SAMPLE_binary.npz', type = str, help = 'path to SNPs NPZ file')
parser.add_argument('--output_folder', default='./Outputs/', type=str, help='folder path to output predictions')
parser.add_argument('--json_file',default = './extracted_data/mutations_cryptic.json', type = str, help = 'path to SNPs name JSON file')
parser.add_argument('--variant_file', default = './data/VARIANTS_SAMPLE.csv', type = str, help = 'path to variant csv file')
parser.add_argument('--raw_mic_file', default='./data/CRyPTIC_reuse_table_20221019.csv', type=str, help='folder path to raw MIC File')
parser.add_argument('--antibiotic', default='MXF', type=str, help='Antibiotic to Extract')
parser.add_argument('--drop_indels', default=False, type=str2bool, help='Choice to Drop Indels in pre-processing')
parser.add_argument('--drop_pe_ppe', default=False, type=str2bool, help='Choice to Drop Mutations in PE/PPE Genes')
parser.add_argument('--raw_files', default=True, type=str2bool, help='Choice to Output RAW Shap files')
args = parser.parse_args()

if __name__ == '__main__':
    #Parsing arguments
    npz_file = args.npz_file
    output_folder = args.output_folder
    json_file = args.json_file
    variant_file = args.variant_file
    mic_file = args.raw_mic_file
    antibiotic = args.antibiotic
    drop_indels = args.drop_indels
    drop_pe_ppe = args.drop_pe_ppe
    raw_files = args.raw_files
    
    #Ensuring output folder exists
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    Path(output_folder+antibiotic).mkdir(parents=True, exist_ok=True)
    
    #Reading in data
    mic_df, _ = read_mic(mic_file, variant_file, antibiotic)
    npz_data = sparse.load_npz(npz_file)
    snp_list = read_list(json_file)
    
    #Running SHAP across DT, RF and XGB selected data
    shap_dt_df = dt_main(npz_data, mic_df, output_folder, snp_list, antibiotic, drop_indels, raw_files)
    shap_rf_df = rf_main(npz_data, mic_df, output_folder, snp_list, antibiotic, drop_indels, raw_files)
    shap_xgb_df = xgb_main(npz_data, mic_df, output_folder, snp_list, antibiotic, drop_indels, raw_files)
    
    #Creating variant dataframe
    var_df = pd.read_csv(variant_file, low_memory = False)
    
    #Creating output dataframe
    output_df = shap_result(shap_dt_df, shap_rf_df, shap_xgb_df, var_df, drop_pe_ppe)
    output_df.to_csv(output_folder+antibiotic+'/'+'SHAP_Avg_'+antibiotic+'.csv', index = False)