select json_build_object (
    'fain', a.fain,
    'piid', a.piid,
    'uri', a.uri,
    'type', a.type,
    'type_desc', a.type_description,
    'desc', a.description,
    'period_of_performance_start_date', a.period_of_performance_start_date,
    'period_of_performance_current_end_date', a.period_of_performance_current_end_date,
    'certified_data', a.certified_date,
    'last_modified_date', a.last_modified_date,
    'total_obligation', a.total_obligation,
    'potential_total_value', a.potential_total_value_of_award,
    'subawards', subaward_count,
    'subaward_amt', total_subaward_amount,
    'funding_agency', json_build_object (
        'cgac', ftt.cgac_code,
        'name', ftt.name,
        'subtier_code', fst.subtier_code,
        'subtier_name', fst.name
    ),
        'awarding_agency', json_build_object (
        'cgac', att.cgac_code,
        'name', att.name,
        'subtier_code', ast.subtier_code,
        'subtier_name', ast.name
    ),
    'recipient', json_build_object (
        'unique_identifier', le.recipient_unique_id, -- DUNS
        'name', le.recipient_name,
        'business_types', le.business_types,
        'business_types_desc', le.business_types_description,
        'business_categories', le.business_categories
    ),
    'recipient_location', json_build_object (
        'country', rl.country_name,
        'state_abbr', rl.state_code,
        'state', rl.state_name,
        'city', rl.city_name,
        'zip', COALESCE(rl.zip4, rl.zip5),
        'congressional_district', rl.congressional_code
    ),
    'place_of_performance', json_build_object (
        'country', pop.country_name,
        'state_abbr', pop.state_code,
        'state', pop.state_name,
        'city', pop.city_name,
        'zip', COALESCE(pop.zip4, pop.zip5),
        'congressional_district', pop.congressional_code
    ),
    'accounting', (
    select json_agg(faa)
    from (
            select
                faa.transaction_obligated_amount obligated_amount,
                json_build_object (
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
                    'federal_account', json_build_object (
                        'agency_identifier', fed_acct.agency_identifier,
                        'main_account_code', fed_acct.main_account_code,
                        'account_title', fed_acct.account_title
                    )
                ) as tas,
                json_build_object (
                    'major_object_class_code', major_object_class,
                    'major_object_class', major_object_class_name,
                    'object_class_code', object_class,
                    'object_class', major_object_class_name,
                    'direct_reimbursable', direct_reimbursable,
                    'direct_reimbursable_name', direct_reimbursable_name
                ) as object_class,
                json_build_object (
                    'program_activity_code', program_activity_code,
                    'program_activity', program_activity_name,
                    'fiscal_year', budget_year
                    ) as program_activity
                from
                    financial_accounts_by_awards faa
                    left join treasury_appropriation_account tas
                    on faa.treasury_account_id = tas.treasury_account_identifier
                    left join federal_account fed_acct
                    on tas.federal_account_id = fed_acct.id
                    left join object_class oc
                    on faa.object_class_id = oc.id
                    left join ref_program_activity pa
                    on faa.program_activity_id = pa.id
                where
                    faa.award_id = a.id
            ) faa
        )
)
from
    awards as a
    /* joins for info about funding agency hierarchy */
    left join agency fa
    on a.funding_agency_id = fa.id
    left join toptier_agency ftt
    on fa.toptier_agency_id = ftt.toptier_agency_id
    left join subtier_agency fst
    on fa.subtier_agency_id = fst.subtier_agency_id
    /* joins for info about awarding agency hierarchy */
    left join agency aa
    on a.awarding_agency_id = aa.id
    left join toptier_agency att
    on aa.toptier_agency_id = att.toptier_agency_id
    left join subtier_agency ast
    on aa.subtier_agency_id = ast.subtier_agency_id
    /* joins for award recipient info */
    left join legal_entity le
    on a.recipient_id = le.legal_entity_id
    left join references_location rl
    on le.location_id =rl.location_id
    /* join for place of performance info */
    left join references_location pop
    on a.place_of_performance_id = pop.location_id
where
/* filter out placeholder awards that don't contain spending info */
a.date_signed is not null
and a.latest_transaction_id is not null
and a.total_obligation is not null
