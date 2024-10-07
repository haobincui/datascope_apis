from connection.client import get_extraction_file_by_job_id
from src.connection.features.extraction.enums.extraction_types import ExtractionTypes

# %% example of get file id
token = "_B5bEEfOIbskMmiD6ADeVfRZZJFdxXJ1T_oGmDY1YTZrrBFEF2irFNbNQRo8jWUW2hM7GGOMROTa_jSO_xRFB_h-XfjIgTKBuQlWK1lJtHrN74R2hfxLVrwQv02tSIRKuSaGDt8q6urwyonLFKpFCGRiAvfcwGTnpjTNHeaPBOlVhDhk9lnyUXwy5SIUxYf4AIRiXTQXISKvp2BRP8yfPEDHqPyTWoWIIn30CWnfbaUN0ou8jxyykwkbp7sUSUJSriZX-f3sPjt0RuRev1c8i0TiO-DV6r9B9lBk-6qEWGWo"

job_id = '0x0855b1662c487eec'
# fild_id = get_extraction_file_by_job_id(job_id=job_id, token=token)

# print(fild_id)




# %% example of saving file by file id
# token = "_j8NwD2Dksu108OA_tiTM9KDGBH50-c7EPLex2P1-YuuHg4_goSfb_43MursbM5moVomSgvEflNCbC2RMTOrXYCp6HvkcRhNvmwnrD4q5DjkC5uwF_2ulkBevKmOLcboSW4sqdzrzr3s4xL53ZrVszFtLQHLjig4nK-qiCP8TGfpGxfo_SievTPoy3PmEzXbpv2_ifMHF8MeqdgBNuIxlUhhpijsHostflQ8G0R36x3qBcYDuJoXMrfB8KvOYeyFZ7L98YuZEmFefQJc3dGV3jpaIyipfFv6ndzeGhUd_9B0"

file_id = 'VjF8MHgwODU1NGEwYjM2ODg3ZTNmfA'
# output_file_name = './testtest2.gz'
# get_extraction_file_by_file_id(extraction_file_id=file_id, output_file_path=output_file_name, token=token)



# %% example of saving file by job id

# token = "_B5bEEfOIbskMmiD6ADeVfRZZJFdxXJ1T_oGmDY1YTZrrBFEF2irFNbNQRo8jWUW2hM7GGOMROTa_jSO_xRFB_h-XfjIgTKBuQlWK1lJtHrN74R2hfxLVrwQv02tSIRKuSaGDt8q6urwyonLFKpFCGRiAvfcwGTnpjTNHeaPBOlVhDhk9lnyUXwy5SIUxYf4AIRiXTQXISKvp2BRP8yfPEDHqPyTWoWIIn30CWnfbaUN0ou8jxyykwkbp7sUSUJSriZX-f3sPjt0RuRev1c8i0TiO-DV6r9B9lBk-6qEWGWo"

job_id = '0x0855b1662c487eec'
extraction_type = ExtractionTypes.ExtractRaw
output_file_path = './output_docs/text_job_id.gz'
res = get_extraction_file_by_job_id(extraction_type, job_id, output_file_path, token)



