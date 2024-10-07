
source activate option_data_processor
nohup python -u get_bond_future_data.py > bond_future_data.log 2>&1 &
echo "get_bond_future_data.py is running..."
conda deactivate

