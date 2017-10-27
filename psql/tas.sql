select json_build_object (
		'label', tas.tas_rendering_label,
		'ata', nullif(tas.allocation_transfer_agency_id, ''),
		'aid', tas.agency_id,
		'bpoa', nullif(tas.beginning_period_of_availability, ''),
		'epoa', nullif(tas.ending_period_of_availability, ''),
		'availability_type_code', nullif(tas.availability_type_code, ''),
		'main_account', tas.main_account_code,
		'sub_account', nullif(tas.sub_account_code, ''),
		'desc', nullif(tas.account_title, ''),
		'budget_function_code', tas.budget_function_code,
		'budget_function_desc', tas.budget_function_title,
		'budget_subfunction_code', tas.budget_subfunction_code,
		'budget_subfunction_desc', tas.budget_subfunction_title,
		'availability_desc', nullif(tas.availability_type_code_description, ''),
		'awarding_agency_code', nullif(ta_awarding.cgac_code, ''),
		'awarding_agency_name', nullif(ta_awarding.name, ''),
		'awarding_agency_abbreviation', nullif(ta_awarding.abbreviation, ''),
		'awarding_agency_fpds_code', nullif(ta_awarding.fpds_code, ''),
		'funding_agency_code', nullif(ta_funding.cgac_code, ''),
		'funding_agency_name', nullif(ta_funding.name, ''),
		'funding_agency_abbreviation', nullif(ta_funding.abbreviation, ''),
		'funding_agency_fpds_code', nullif(ta_funding.fpds_code, ''),
		'federal_account', json_build_object (
			'agency_identifier', fa.agency_identifier,
			'main_account_code', fa.main_account_code,
			'account_title', fa.account_title
		))
from federal_account fa
left join treasury_appropriation_account tas
on fa.id = tas.federal_account_id
left join toptier_agency ta_awarding
on tas.awarding_toptier_agency_id = ta_awarding.toptier_agency_id
left join toptier_agency ta_funding
on tas.funding_toptier_agency_Id = ta_funding.toptier_agency_id