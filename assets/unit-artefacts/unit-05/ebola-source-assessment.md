# Unit 5 source assessment: 2014 West African Ebola data

## Investigation question

Can the `cmrivers/ebola` repository support a defensible historical analysis of
reported Ebola cases and deaths during the 2014 West African outbreak?

## Data smell test

| Test | Finding | Judgement |
|---|---|---|
| Is the author identifiable and contactable? | The repository identifies Caitlin Rivers, gives institutional context and supplies contact routes. | Yes |
| Was the data updated and checked? | The commit history and proofreading tools show maintenance activity, but the maintainer states that updates stopped on 15 December 2015. | Qualified |
| Is acquisition documented? | The README attributes files to WHO situation reports and national health ministries. It also states that some records were digitised manually or with Tabula. Detailed sampling and verification methods are not supplied for every file. | Partial |
| Can another source validate it? | WHO situation reports and the country-specific health-ministry sources named in the README provide possible comparison points. | Yes, but links and historical availability must be checked |
| Does the data appear plausible? | The country time series is structurally consistent, but it contains substantial missingness and downward revisions in cumulative totals. These are plausible reporting artefacts, not proof of error-free data. | Qualified |

## Reproducible profile

The Python profile found 122 rows and 18 columns covering 22 March 2014 to
5 January 2015. It found no duplicate dates and no malformed rows. However,
1,214 of 2,196 cells (55.28%) were blank, and 32 downward changes appeared
across the cumulative case and death series when ordered chronologically.

Blank cells were retained because absence from a situation report is not the
same as a recorded value of zero. Downward changes were flagged rather than
overwritten because surveillance totals may be revised after cases are
reclassified or duplicate reports are reconciled. Any substantive analysis
should therefore document missingness, compare important figures with the
original reports and avoid presenting the repository as current data.

## Conclusion

The repository is suitable for a historical learning exercise because it has
clear provenance, transparent cautions and reproducible files. It is not
suitable for current outbreak monitoring. Its strongest use in this portfolio
is to demonstrate source evaluation, profiling and cautious transformation,
not to claim definitive epidemiological findings.

## Sources

- Kazil, J. and Jarmul, K. (2016b) ‘Wrangle your data with Python’, *O’Reilly*,
  24 August. <https://www.oreilly.com/content/wrangle-your-data-with-python/>
- Rivers, C. (no date) *cmrivers/ebola* [Dataset]. GitHub.
  <https://github.com/cmrivers/ebola>
