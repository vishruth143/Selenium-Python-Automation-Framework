# pylint: disable=[missing-module-docstring, missing-class-docstring, missing-function-docstring]
# pylint: disable=[line-too-long, logging-fstring-interpolation, import-error, too-many-public-methods, superfluous-parens]

import re
import pytest

from framework.utilities.custom_logger import Logger

log = Logger(file_id=__name__.rsplit(".", 1)[1])


@pytest.mark.restcountries_data
class TestRestCountriesData:

    """
    Data Quality Test Suite — REST Countries API
    =============================================
    Target : https://restcountries.com/v3.1/all
    Tests  : Completeness, Schema, Type/Format, Range/Boundary,
             Integrity, Uniqueness, Pandas Statistical Analysis

    All HTTP calls are made once per session (see tests/data/conftest.py).
    Individual tests receive pre-loaded fixtures — no extra network calls.
    """

    # ------------------------------------------------------------------
    # 1. DATA COMPLETENESS
    # ------------------------------------------------------------------

    def test_total_country_count_within_expected_range(self, all_countries, data_config):
        """
        Test #01 : Verify total country count is between 245 and 260.
        Catches accidental bulk deletions or import failures.
        """
        try:
            log.info(50 * '*')
            log.info("Test #01 : Verify total country count is within expected range.")
            log.info(50 * '*')

            exp = data_config["expected"]
            total = len(all_countries)
            log.info(f"Total countries returned by API: {total}")
            log.info(f"Expected range: {exp['total_countries_min']} – {exp['total_countries_max']}")

            assert exp["total_countries_min"] <= total <= exp["total_countries_max"], (
                f"Expected between {exp['total_countries_min']} and "
                f"{exp['total_countries_max']} countries, got {total}"
            )
            log.info(f"PASS — {total} countries is within the expected range.")
            log.info("Test #01 : Verify total country count - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #01 : Verify total country count - Failed")
            raise

    def test_no_country_has_empty_common_name(self, all_countries):
        """
        Test #02 : Verify no country has a blank common name.
        """
        try:
            log.info(50 * '*')
            log.info("Test #02 : Verify no country has an empty common name.")
            log.info(50 * '*')

            empty = [
                c.get("cca3", "UNKNOWN")
                for c in all_countries
                if not c.get("name", {}).get("common", "").strip()
            ]
            log.info(f"Countries with empty common name: {empty if empty else 'None'}")
            assert not empty, f"Countries with empty common name: {empty}"
            log.info("PASS — All countries have a non-empty common name.")
            log.info("Test #02 : Verify no empty common name - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #02 : Verify no empty common name - Failed")
            raise

    def test_no_country_has_empty_cca2(self, all_countries):
        """
        Test #03 : Verify every country has a 2-letter ISO code (cca2).
        """
        try:
            log.info(50 * '*')
            log.info("Test #03 : Verify no country has an empty cca2 code.")
            log.info(50 * '*')

            empty = [
                c.get("name", {}).get("common", "?")
                for c in all_countries
                if not c.get("cca2", "").strip()
            ]
            log.info(f"Countries missing cca2: {empty if empty else 'None'}")
            assert not empty, f"Countries missing cca2: {empty}"
            log.info("PASS — All countries have a non-empty cca2.")
            log.info("Test #03 : Verify no empty cca2 - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #03 : Verify no empty cca2 - Failed")
            raise

    def test_no_country_has_empty_cca3(self, all_countries):
        """
        Test #04 : Verify every country has a 3-letter ISO code (cca3).
        """
        try:
            log.info(50 * '*')
            log.info("Test #04 : Verify no country has an empty cca3 code.")
            log.info(50 * '*')

            empty = [
                c.get("name", {}).get("common", "?")
                for c in all_countries
                if not c.get("cca3", "").strip()
            ]
            log.info(f"Countries missing cca3: {empty if empty else 'None'}")
            assert not empty, f"Countries missing cca3: {empty}"
            log.info("PASS — All countries have a non-empty cca3.")
            log.info("Test #04 : Verify no empty cca3 - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #04 : Verify no empty cca3 - Failed")
            raise

    def test_no_country_has_empty_region(self, all_countries):
        """
        Test #05 : Verify every country belongs to a region.
        """
        try:
            log.info(50 * '*')
            log.info("Test #05 : Verify no country has an empty region.")
            log.info(50 * '*')

            empty = [
                c.get("name", {}).get("common", "?")
                for c in all_countries
                if not c.get("region", "").strip()
            ]
            log.info(f"Countries missing region: {empty if empty else 'None'}")
            assert not empty, f"Countries missing region: {empty}"
            log.info("PASS — All countries have a region assigned.")
            log.info("Test #05 : Verify no empty region - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #05 : Verify no empty region - Failed")
            raise

    # ------------------------------------------------------------------
    # 2. SCHEMA VALIDATION
    # ------------------------------------------------------------------

    def test_required_fields_present_in_every_country(self, all_countries):
        """
        Test #06 : Verify every country object contains required top-level fields.
        Catches API schema regressions — if the API drops a field, this fails immediately.
        """
        try:
            log.info(50 * '*')
            log.info("Test #06 : Verify required fields present in every country object.")
            log.info(50 * '*')

            required = {"name", "cca2", "cca3", "region", "population", "flags"}
            violations = []
            for country in all_countries:
                missing = required - country.keys()
                if missing:
                    violations.append(
                        f"{country.get('name', {}).get('common', '?')} missing: {missing}"
                    )

            log.info(f"Required fields checked: {required}")
            log.info(f"Schema violations found: {len(violations)}")
            assert not violations, "Schema violations:\n" + "\n".join(violations)
            log.info("PASS — All countries contain required fields.")
            log.info("Test #06 : Verify required fields - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #06 : Verify required fields - Failed")
            raise

    def test_name_field_has_common_and_official(self, all_countries):
        """
        Test #07 : Verify name object contains both 'common' and 'official' sub-fields.
        """
        try:
            log.info(50 * '*')
            log.info("Test #07 : Verify name.common and name.official present for every country.")
            log.info(50 * '*')

            violations = []
            for c in all_countries:
                name = c.get("name", {})
                if "common" not in name or "official" not in name:
                    violations.append(c.get("cca3", "?"))

            log.info(f"Violations found: {violations if violations else 'None'}")
            assert not violations, f"Countries missing name.common/official: {violations}"
            log.info("PASS — All countries have name.common and name.official.")
            log.info("Test #07 : Verify name sub-fields - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #07 : Verify name sub-fields - Failed")
            raise

    def test_population_is_non_negative_integer(self, all_countries):
        """
        Test #08 : Verify population is an integer >= 0 for every country.
        """
        try:
            log.info(50 * '*')
            log.info("Test #08 : Verify population is a non-negative integer.")
            log.info(50 * '*')

            violations = []
            for c in all_countries:
                pop = c.get("population")
                if not isinstance(pop, int) or pop < 0:
                    violations.append(
                        f"{c.get('name', {}).get('common', '?')}: population={pop}"
                    )

            log.info(f"Population violations: {violations if violations else 'None'}")
            assert not violations, "Invalid population values:\n" + "\n".join(violations)
            log.info("PASS — All population values are valid non-negative integers.")
            log.info("Test #08 : Verify population type - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #08 : Verify population type - Failed")
            raise

    def test_flags_field_has_png_and_svg(self, all_countries):
        """
        Test #09 : Verify flags object contains both 'png' and 'svg' URL fields.
        """
        try:
            log.info(50 * '*')
            log.info("Test #09 : Verify flags.png and flags.svg present for every country.")
            log.info(50 * '*')

            violations = []
            for c in all_countries:
                flags = c.get("flags", {})
                if "png" not in flags or "svg" not in flags:
                    violations.append(c.get("name", {}).get("common", "?"))

            log.info(f"Violations: {violations if violations else 'None'}")
            assert not violations, f"Countries missing flag URLs: {violations}"
            log.info("PASS — All countries have both png and svg flag URLs.")
            log.info("Test #09 : Verify flag URLs schema - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #09 : Verify flag URLs schema - Failed")
            raise

    # ------------------------------------------------------------------
    # 3. DATA TYPE & FORMAT VALIDATION
    # ------------------------------------------------------------------

    def test_cca2_is_two_uppercase_letters(self, all_countries):
        """
        Test #10 : Verify cca2 matches ^[A-Z]{2}$ (ISO 3166-1 alpha-2 format).
        """
        try:
            log.info(50 * '*')
            log.info("Test #10 : Verify cca2 format is exactly 2 uppercase letters.")
            log.info(50 * '*')

            pattern = re.compile(r'^[A-Z]{2}$')
            violations = []
            for c in all_countries:
                code = c.get("cca2", "")
                if not pattern.match(code):
                    violations.append(f"{c.get('name', {}).get('common', '?')}: cca2='{code}'")

            log.info(f"cca2 format violations: {violations if violations else 'None'}")
            assert not violations, "Invalid cca2 codes:\n" + "\n".join(violations)
            log.info("PASS — All cca2 codes are correctly formatted.")
            log.info("Test #10 : Verify cca2 format - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #10 : Verify cca2 format - Failed")
            raise

    def test_cca3_is_three_uppercase_letters(self, all_countries):
        """
        Test #11 : Verify cca3 matches ^[A-Z]{3}$ (ISO 3166-1 alpha-3 format).
        """
        try:
            log.info(50 * '*')
            log.info("Test #11 : Verify cca3 format is exactly 3 uppercase letters.")
            log.info(50 * '*')

            pattern = re.compile(r'^[A-Z]{3}$')
            violations = []
            for c in all_countries:
                code = c.get("cca3", "")
                if not pattern.match(code):
                    violations.append(f"{c.get('name', {}).get('common', '?')}: cca3='{code}'")

            log.info(f"cca3 format violations: {violations if violations else 'None'}")
            assert not violations, "Invalid cca3 codes:\n" + "\n".join(violations)
            log.info("PASS — All cca3 codes are correctly formatted.")
            log.info("Test #11 : Verify cca3 format - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #11 : Verify cca3 format - Failed")
            raise

    def test_currency_codes_are_three_uppercase_letters(self, all_countries):
        """
        Test #12 : Verify all currency codes match ^[A-Z]{3}$ (ISO 4217 format).
        """
        try:
            log.info(50 * '*')
            log.info("Test #12 : Verify all currency codes are 3 uppercase letters (ISO 4217).")
            log.info(50 * '*')

            pattern = re.compile(r'^[A-Z]{3}$')
            violations = []
            for c in all_countries:
                for code in c.get("currencies", {}).keys():
                    if not pattern.match(code):
                        violations.append(
                            f"{c.get('name', {}).get('common', '?')}: currency='{code}'"
                        )

            log.info(f"Currency code violations: {violations if violations else 'None'}")
            assert not violations, "Invalid currency codes:\n" + "\n".join(violations)
            log.info("PASS — All currency codes are valid ISO 4217 format.")
            log.info("Test #12 : Verify currency code format - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #12 : Verify currency code format - Failed")
            raise

    def test_timezones_format(self, all_countries):
        """
        Test #13 : Verify all timezones match UTC, UTC+HH:MM, or UTC-HH:MM.
        """
        try:
            log.info(50 * '*')
            log.info("Test #13 : Verify all timezone values follow UTC format.")
            log.info(50 * '*')

            pattern = re.compile(r'^UTC([+-]\d{2}:\d{2})?$')
            violations = []
            for c in all_countries:
                for tz in c.get("timezones", []):
                    if not pattern.match(tz):
                        violations.append(
                            f"{c.get('name', {}).get('common', '?')}: tz='{tz}'"
                        )

            log.info(f"Timezone format violations: {violations if violations else 'None'}")
            assert not violations, "Invalid timezone formats:\n" + "\n".join(violations)
            log.info("PASS — All timezone values are correctly formatted.")
            log.info("Test #13 : Verify timezone format - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #13 : Verify timezone format - Failed")
            raise

    def test_flag_urls_start_with_https(self, all_countries):
        """
        Test #14 : Verify all flag PNG and SVG URLs start with 'https://'.
        """
        try:
            log.info(50 * '*')
            log.info("Test #14 : Verify all flag URLs start with https://.")
            log.info(50 * '*')

            violations = []
            for c in all_countries:
                flags = c.get("flags", {})
                for fmt in ("png", "svg"):
                    url = flags.get(fmt, "")
                    if url and not url.startswith("https://"):
                        violations.append(
                            f"{c.get('name', {}).get('common', '?')}: {fmt} url='{url}'"
                        )

            log.info(f"Flag URL violations: {violations if violations else 'None'}")
            assert not violations, "Invalid flag URLs:\n" + "\n".join(violations)
            log.info("PASS — All flag URLs use HTTPS.")
            log.info("Test #14 : Verify flag URL protocol - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #14 : Verify flag URL protocol - Failed")
            raise

    # ------------------------------------------------------------------
    # 4. RANGE / BOUNDARY VALIDATION
    # ------------------------------------------------------------------

    def test_latlng_within_valid_geographic_range(self, all_countries, data_config):
        """
        Test #15 : Verify latitude is -90 to +90 and longitude is -180 to +180.
        Catches coordinate entry errors or data corruption.
        """
        try:
            log.info(50 * '*')
            log.info("Test #15 : Verify lat/lng coordinates are within valid geographic range.")
            log.info(50 * '*')

            exp = data_config["expected"]
            violations = []
            for c in all_countries:
                latlng = c.get("latlng", [])
                if len(latlng) == 2:
                    lat, lng = latlng
                    if not (exp["lat_min"] <= lat <= exp["lat_max"]):
                        violations.append(
                            f"{c.get('name', {}).get('common', '?')}: lat={lat} out of range"
                        )
                    if not (exp["lng_min"] <= lng <= exp["lng_max"]):
                        violations.append(
                            f"{c.get('name', {}).get('common', '?')}: lng={lng} out of range"
                        )

            log.info(f"Coordinate violations: {violations if violations else 'None'}")
            assert not violations, "Out-of-range coordinates:\n" + "\n".join(violations)
            log.info("PASS — All lat/lng coordinates are within valid ranges.")
            log.info("Test #15 : Verify lat/lng range - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #15 : Verify lat/lng range - Failed")
            raise

    def test_area_is_positive_when_present(self, all_countries):
        """
        Test #16 : Verify area, when provided, is a positive number.
        """
        try:
            log.info(50 * '*')
            log.info("Test #16 : Verify area value is positive when present.")
            log.info(50 * '*')

            violations = []
            for c in all_countries:
                area = c.get("area")
                if area is not None and area < 0:
                    violations.append(
                        f"{c.get('name', {}).get('common', '?')}: area={area}"
                    )

            log.info(f"Negative area violations: {violations if violations else 'None'}")
            assert not violations, "Negative area values:\n" + "\n".join(violations)
            log.info("PASS — All area values are non-negative.")
            log.info("Test #16 : Verify area range - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #16 : Verify area range - Failed")
            raise

    # ------------------------------------------------------------------
    # 5. DATA INTEGRITY
    # ------------------------------------------------------------------

    def test_border_codes_reference_valid_countries(self, all_countries):
        """
        Test #17 : Verify every border cca3 code refers to a real country in the dataset.
        Catches broken cross-references (orphan border entries).
        """
        try:
            log.info(50 * '*')
            log.info("Test #17 : Verify all border codes reference existing countries.")
            log.info(50 * '*')

            all_cca3 = {c.get("cca3") for c in all_countries}
            violations = []
            for c in all_countries:
                for border in c.get("borders", []):
                    if border not in all_cca3:
                        violations.append(
                            f"{c.get('name', {}).get('common', '?')}: "
                            f"border '{border}' not found in dataset"
                        )

            log.info(f"Border integrity violations: {violations if violations else 'None'}")
            assert not violations, "Broken border references:\n" + "\n".join(violations)
            log.info("PASS — All border codes reference valid countries.")
            log.info("Test #17 : Verify border integrity - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #17 : Verify border integrity - Failed")
            raise

    def test_all_expected_regions_present(self, all_countries, data_config):
        """
        Test #18 : Verify all 6 world regions (Africa, Americas, Asia, Europe,
        Oceania, Antarctic) are represented.
        """
        try:
            log.info(50 * '*')
            log.info("Test #18 : Verify all expected world regions are present.")
            log.info(50 * '*')

            expected_regions = set(data_config["expected"]["regions"])
            actual_regions = {c.get("region", "") for c in all_countries}
            missing = expected_regions - actual_regions

            log.info(f"Expected regions : {sorted(expected_regions)}")
            log.info(f"Actual regions   : {sorted(r for r in actual_regions if r)}")
            log.info(f"Missing regions  : {missing if missing else 'None'}")

            assert not missing, f"Missing regions in dataset: {missing}"
            log.info("PASS — All expected world regions are present.")
            log.info("Test #18 : Verify region coverage - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #18 : Verify region coverage - Failed")
            raise

    # ------------------------------------------------------------------
    # 6. UNIQUENESS VALIDATION
    # ------------------------------------------------------------------

    def test_cca2_codes_are_unique(self, countries_df):
        """
        Test #19 : Verify no two countries share the same cca2 code.
        """
        try:
            log.info(50 * '*')
            log.info("Test #19 : Verify cca2 codes are unique across all countries.")
            log.info(50 * '*')

            duplicates = countries_df[
                countries_df.duplicated("cca2", keep=False)
            ]["cca2"].tolist()

            log.info(f"Duplicate cca2 codes: {duplicates if duplicates else 'None'}")
            assert not duplicates, f"Duplicate cca2 codes found: {duplicates}"
            log.info("PASS — All cca2 codes are unique.")
            log.info("Test #19 : Verify cca2 uniqueness - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #19 : Verify cca2 uniqueness - Failed")
            raise

    def test_cca3_codes_are_unique(self, countries_df):
        """
        Test #20 : Verify no two countries share the same cca3 code.
        """
        try:
            log.info(50 * '*')
            log.info("Test #20 : Verify cca3 codes are unique across all countries.")
            log.info(50 * '*')

            duplicates = countries_df[
                countries_df.duplicated("cca3", keep=False)
            ]["cca3"].tolist()

            log.info(f"Duplicate cca3 codes: {duplicates if duplicates else 'None'}")
            assert not duplicates, f"Duplicate cca3 codes found: {duplicates}"
            log.info("PASS — All cca3 codes are unique.")
            log.info("Test #20 : Verify cca3 uniqueness - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #20 : Verify cca3 uniqueness - Failed")
            raise

    def test_country_names_are_unique(self, countries_df):
        """
        Test #21 : Verify no two countries share the same common name.
        """
        try:
            log.info(50 * '*')
            log.info("Test #21 : Verify country common names are unique.")
            log.info(50 * '*')

            duplicates = countries_df[
                countries_df.duplicated("name", keep=False)
            ]["name"].tolist()

            log.info(f"Duplicate names: {duplicates if duplicates else 'None'}")
            assert not duplicates, f"Duplicate country names found: {duplicates}"
            log.info("PASS — All country names are unique.")
            log.info("Test #21 : Verify country name uniqueness - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #21 : Verify country name uniqueness - Failed")
            raise

    # ------------------------------------------------------------------
    # 7. PANDAS STATISTICAL ANALYSIS
    # ------------------------------------------------------------------

    def test_population_statistics_are_sensible(self, countries_df):
        """
        Test #22 : Verify population statistics using pandas.
        - Mean population must be > 0
        - Max population must be < 2 billion (believable upper bound)
        - At least 1 country must have population > 100 million
        """
        try:
            log.info(50 * '*')
            log.info("Test #22 : Verify population statistics are within sensible bounds.")
            log.info(50 * '*')

            pop = countries_df["population"]
            log.info(f"Population stats: min={pop.min():,} | max={pop.max():,} | "
                     f"mean={pop.mean():,.0f} | median={pop.median():,.0f}")

            assert pop.mean() > 0, "Mean population must be > 0"
            assert pop.max() < 2_000_000_000, (
                f"Max population {pop.max():,} exceeds 2 billion — suspicious value"
            )
            large_country_count = int((pop > 100_000_000).sum())
            assert large_country_count >= 1, (
                "Expected at least 1 country with population > 100 million"
            )
            log.info(f"Countries with population > 100M: {large_country_count}")
            log.info("PASS — Population statistics are within expected bounds.")
            log.info("Test #22 : Verify population statistics - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #22 : Verify population statistics - Failed")
            raise

    def test_region_distribution_is_balanced(self, countries_df):
        """
        Test #23 : Verify each region has at least 3 countries using pandas groupby.
        """
        try:
            log.info(50 * '*')
            log.info("Test #23 : Verify region distribution — each region has >= 3 countries.")
            log.info(50 * '*')

            dist = countries_df[countries_df["region"] != ""].groupby("region").size()
            log.info(f"Region distribution:\n{dist.to_string()}")

            violations = []
            for region, count in dist.items():
                if count < 3:
                    violations.append(f"Region '{region}' has only {count} countries")

            assert not violations, "\n".join(violations)
            log.info("PASS — All regions have at least 3 countries.")
            log.info("Test #23 : Verify region distribution - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #23 : Verify region distribution - Failed")
            raise

    def test_no_null_names_in_dataframe(self, countries_df):
        """
        Test #24 : Verify no country has a null or empty name in the DataFrame.
        """
        try:
            log.info(50 * '*')
            log.info("Test #24 : Pandas null check — no country name should be null/empty.")
            log.info(50 * '*')

            null_names = countries_df[
                countries_df["name"].isnull() | (countries_df["name"] == "")
            ]
            log.info(f"Null/empty name rows: {len(null_names)}")
            assert null_names.empty, (
                f"Null/empty names found:\n{null_names[['cca3', 'name']].to_string()}"
            )
            log.info("PASS — No null or empty country names in DataFrame.")
            log.info("Test #24 : Verify no null names - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #24 : Verify no null names - Failed")
            raise

    def test_dataset_has_sufficient_subregions(self, countries_df):
        """
        Test #25 : Verify the dataset contains at least 10 distinct subregions.
        """
        try:
            log.info(50 * '*')
            log.info("Test #25 : Verify dataset contains at least 10 distinct subregions.")
            log.info(50 * '*')

            subregion_counts = (
                countries_df[countries_df["subregion"] != ""]
                .groupby("subregion")
                .size()
            )
            total_subregions = len(subregion_counts)
            log.info(f"Total distinct subregions found: {total_subregions}")
            log.info(f"Subregions:\n{subregion_counts.to_string()}")

            assert total_subregions >= 10, (
                f"Expected at least 10 subregions, got {total_subregions}"
            )
            log.info("PASS — Dataset has sufficient subregion coverage.")
            log.info("Test #25 : Verify subregion count - Passed")

        except Exception as e:
            log.error(f"Error: {e}")
            log.info("Test #25 : Verify subregion count - Failed")
            raise
