#!/usr/bin/env python3
"""Build the Google Calendar import file from the festa-major source list.

The calendar uses all-day, yearly recurring events.  `source_url` is the
direct bTV programme page supplied in Festes_URLs.ini; it is included both in
the event URL and the description so it remains usable after import.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path


YEAR = 2026
OUTPUT = Path("Festes_Majors_Barcelona.ics")

# (display name, Barcelona location, first day as MM-DD, source URL slug)
# Dates are the 2026 edition start dates; RRULE makes each entry recur yearly.
FESTES = [
    ("Festa Major de Vallvidrera", "Vallvidrera, Barcelona", "09-12", "festa-major-vallvidrera-programa"),
    ("Festa Major dels Indians", "El Camp de l'Arpa del Clot, Barcelona", "09-19", "festa-major-indians-programa"),
    ("Festes de la Mercè", "Barcelona", "09-24", "festa-major-barri-merce-programa"),
    ("Festa Major de Montbau", "Montbau, Barcelona", "10-02", "festa-major-montbau-programa"),
    ("Festa Major d'Hostafrancs", "Hostafrancs, Barcelona", "10-03", "festa-major-hostafrancs-programa"),
    ("Festa del Roser", "La Rambla, Barcelona", "10-05", "festa-roser-barcelona"),
    ("Festa Major de Vilapicina i la Torre Llobeta", "Vilapicina i la Torre Llobeta, Barcelona", "10-10", "festa-major-vilapicina-torre-llobeta-programa"),
    ("Festa Major del Congrés", "El Congrés i els Indians, Barcelona", "10-10", "festa-major-congres-programa"),
    ("Festa Major de l'Esquerra de l'Eixample", "L'Esquerra de l'Eixample, Barcelona", "10-10", "festa-major-esquerra-eixample-programa"),
    ("Festa Major de Sarrià", "Sarrià, Barcelona", "10-02", "festa-major-sarria-programa"),
    ("Festa Major de les Corts", "Les Corts, Barcelona", "10-06", "festa-major-corts-programa"),
    ("Festa Major de Canyelles", "Canyelles, Barcelona", "04-25", "festa-major-canyelles-programa"),
    ("Festa Major del Clot i Camp de l'Arpa", "El Clot i Camp de l'Arpa, Barcelona", "11-07", "programa-festa-major-clot-camp-de-larpa"),
    ("Festa Major de la Verneda", "La Verneda i la Pau, Barcelona", "11-07", "festa-major-verneda-programa"),
    ("Festa Major de la Sagrera", "La Sagrera, Barcelona", "11-14", "festa-major-sagrera-programa"),
    ("Festa Major de Sant Andreu", "Sant Andreu de Palomar, Barcelona", "11-28", "festa-major-sant-andreu-programa"),
    ("Festa Major de Sant Antoni", "Sant Antoni, Barcelona", "01-17", "festa-major-sant-antoni"),
    ("Festes de Santa Eulàlia", "Barcelona", "02-06", "festes-santa-eulalia-barcelona-programa"),
    ("Festes de Santa Madrona", "Poble-sec, Barcelona", "03-14", "festes-santa-madrona-poble-sec-programa"),
    ("Festes de Sant Josep Oriol", "Barri Gòtic, Barcelona", "03-21", "festes-sant-josep-oriol-barcelona"),
    ("Festa Major de la Sagrada Família", "Sagrada Família, Barcelona", "04-23", "festa-major-sagrada-familia-programa"),
    ("Festa Major del Guinardó", "El Guinardó, Barcelona", "05-02", "festa-major-guinardo-programa"),
    ("Festa Major de Porta", "Porta, Barcelona", "05-15", "agenda-festa-major-porta-programa"),
    ("Festa Major del Bon Pastor", "Bon Pastor, Barcelona", "05-15", "festa-major-bon-pastor-programa"),
    ("Festa Major de Navas", "Navas, Barcelona", "05-22", "festa-major-navas-programa"),
    ("Festes del Gòtic", "Barri Gòtic, Barcelona", "05-08", "festes-gotic-barcelona-programa"),
    ("Festa Major de Nou Barris", "Nou Barris, Barcelona", "05-13", "festa-major-nou-barris-programa"),
    ("Festa Major de la Dreta de l'Eixample", "La Dreta de l'Eixample, Barcelona", "05-22", "festa-major-dreta-eixample-programa"),
    ("Festa Major del passatge Pellicer", "Vallcarca i els Penitents, Barcelona", "05-22", "festa-major-passatge-pellicer-programa"),
    ("Festa Major de la Prosperitat", "La Prosperitat, Barcelona", "05-22", "festa-major-prosperitat-programa"),
    ("Festa Major de la Trinitat Vella", "Trinitat Vella, Barcelona", "05-29", "festa-major-trinitat-vella-programa"),
    ("Festa Major del Besòs i el Maresme", "El Besòs i el Maresme, Barcelona", "06-05", "festa-major-besos-maresme-programa"),
    ("Festa Major del Putxet", "El Putxet i el Farró, Barcelona", "06-12", "festa-major-putxet-programa"),
    ("Festa Major de Sant Genís dels Agudells", "Sant Genís dels Agudells, Barcelona", "06-12", "festa-major-sant-genis-agudells-programa"),
    ("Festa Major del Paraguai-Perú", "La Verneda i la Pau, Barcelona", "06-12", "festa-major-paraguai-peru-programa"),
    ("Festa Major de la Teixonera, Mas Falcó i Penitents", "La Teixonera, Barcelona", "06-12", "festa-major-teixonera-mas-falco-penitents-programa"),
    ("Festa Major de Sant Gervasi", "Sant Gervasi, Barcelona", "06-13", "festa-major-sant-gervasi-programa"),
    ("Festa Major del Fort Pienc", "Fort Pienc, Barcelona", "06-13", "festa-major-fort-pienc-programa"),
    ("Festa Major del Baix Guinardó", "Baix Guinardó, Barcelona", "06-19", "festa-major-baix-guinardo-programa"),
]

# The remaining programme pages all correspond to the summer festa-major season.
SUMMER_SLUGS = [
    ("Festa Major del Turó de la Peira", "Turó de la Peira, Barcelona", "06-19", "festa-major-turo-peira-programa"),
    ("Festa Major de la Font d'en Fargues", "La Font d'en Fargues, Barcelona", "06-19", "festa-major-font-fargues-programa"),
    ("Festa Major de la Trinitat Nova", "Trinitat Nova, Barcelona", "06-19", "festa-major-trinitat-nova-programa"),
    ("Festa Major del Baró de Viver", "Baró de Viver, Barcelona", "06-19", "festa-major-baro-viver-programa"),
    ("Festa Major de Ciutat Meridiana", "Ciutat Meridiana, Barcelona", "06-19", "festa-major-ciutat-meridiana-programa"),
    ("Festa Major de la Palmera", "La Sagrera, Barcelona", "06-19", "festa-major-palmera-barcelona-programa"),
    ("Festa Major de la Pau", "La Verneda i la Pau, Barcelona", "06-19", "festa-major-pau-programa"),
    ("Festa Major de Can Baró", "Can Baró, Barcelona", "06-19", "festa-major-can-baro-programa"),
    ("Festa Major del Coll", "El Coll, Barcelona", "06-19", "festa-major-coll-programa"),
    ("Festa Major de les Roquetes", "Les Roquetes, Barcelona", "06-19", "festa-major-roquetes-programa"),
    ("Festa Major de la Guineueta", "La Guineueta, Barcelona", "06-19", "festa-major-guineueta-programa"),
    ("Festa Major de la Font de la Guatlla", "La Font de la Guatlla, Barcelona", "06-19", "festa-major-font-guatlla-programa"),
    ("Festa Major de la Vall d'Hebron", "La Vall d'Hebron, Barcelona", "06-19", "festa-major-vall-hebron-programa"),
    ("Festa Major de Can Peguera", "Can Peguera, Barcelona", "06-19", "festa-major-can-peguera-programa"),
    ("Festa Major de la Vila Olímpica", "La Vila Olímpica del Poblenou, Barcelona", "06-19", "festa-major-vila-olimpica-programa"),
    ("Festa Major de Mas Sauró", "Mas Sauró, Barcelona", "06-19", "festa-major-mas-sauro-programa"),
    ("Festa Major de Vallbona", "Vallbona, Barcelona", "06-19", "festa-major-vallbona-programa"),
    ("Festa Major de la Vinya", "La Vinya, Barcelona", "06-20", "festa-major-de-la-vinya-2026-dates-i-programa"),
    ("Festa Major de Font del Gos", "Font del Gos, Barcelona", "06-20", "festa-major-font-gos-programa"),
    ("Festa Major del Casc Antic", "Casc Antic, Barcelona", "06-20", "festa-major-casc-antic-programa"),
    ("Festa Major de Can Clos", "Can Clos, Barcelona", "06-20", "festa-major-de-can-clos-2026-dates-i-programa"),
    ("Festa Major de Torre Baró", "Torre Baró, Barcelona", "06-20", "festa-major-torre-baro-programa"),
    ("Festa Major del Camp d'en Grassot i Gràcia Nova", "Camp d'en Grassot i Gràcia Nova, Barcelona", "06-20", "festa-major-camp-grassot-gracia-nova-programa"),
    ("Festa Major del Rectoret", "El Rectoret, Barcelona", "06-20", "festa-major-rectoret-programa"),
    ("Festa Major del Carmel", "El Carmel, Barcelona", "07-10", "festa-major-carmel-programa"),
    ("Festa Major del Raval", "El Raval, Barcelona", "07-16", "festa-major-raval"),
    ("Festa Major de Sant Cristòfol", "Barcelona", "07-10", "festa-major-de-sant-cristofol-2026-programa-i-dates-de-les-festes"),
    ("Festa Major de la Marina", "La Marina de Port, Barcelona", "07-17", "festa-major-marina-programa"),
    ("Festa de les Cases Barates", "La Marina de Port, Barcelona", "07-17", "festa-cases-barates-la-marina-barcelona-programa"),
    ("Festa Major del Poble-sec", "Poble-sec, Barcelona", "07-17", "festa-major-poble-sec"),
    ("Festa Major de la Clota", "La Clota, Barcelona", "07-17", "festa-major-la-clota-programa"),
    ("Festes de Sant Roc", "Barri Gòtic, Barcelona", "08-14", "festes-sant-roc-barcelona"),
    ("Festes de Gràcia", "Vila de Gràcia, Barcelona", "08-15", "festes-gracia-programa"),
    ("Festes de Sants", "Sants, Barcelona", "08-21", "festes-sants-programa"),
    ("Festa Major de la Font del Mont", "La Font del Mont, Barcelona", "08-28", "festa-major-font-mont-programa"),
    ("Festa Major de Mas Guimbau-Can Castellví", "Mas Guimbau-Can Castellví, Barcelona", "08-28", "festa-major-mas-guimbau-can-castellvi-programa"),
    ("Festa Major de la Bordeta", "La Bordeta, Barcelona", "09-04", "festa-major-bordeta-programa"),
    ("Festa Major de Vallcarca", "Vallcarca, Barcelona", "09-04", "festa-major-vallcarca-programa"),
    ("Festa Major d'Horta", "Horta, Barcelona", "09-04", "festa-major-horta-programa"),
    ("Festa Major de la Salut", "La Salut, Barcelona", "08-15", "festa-major-salut-programa"),
    ("Festa Major del Farró", "El Putxet i el Farró, Barcelona", "09-11", "festa-major-farro-programa"),
]


def escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line: str) -> str:
    """Fold an iCalendar content line at the RFC 5545 octet limit."""
    parts = []
    while len(line.encode("utf-8")) > 75:
        size = 75
        while len(line[:size].encode("utf-8")) > 75:
            size -= 1
        parts.append(line[:size])
        line = " " + line[size:]
    return "\r\n".join(parts + [line])


def event_lines(name: str, location: str, month_day: str, slug: str) -> list[str]:
    start = date.fromisoformat(f"{YEAR}-{month_day}")
    url = f"https://beteve.cat/agenda/{slug}/"
    return [
        "BEGIN:VEVENT",
        f"UID:{slug}@gcal-festes-majors.local",
        "DTSTAMP:20260920T000000Z",
        f"DTSTART;VALUE=DATE:{start:%Y%m%d}",
        f"DTEND;VALUE=DATE:{(start + timedelta(days=1)):%Y%m%d}",
        "RRULE:FREQ=YEARLY",
        f"SUMMARY:{escape(f'🎊 | {name} {start:%m/%d}')}",
        f"LOCATION:{escape(location)}",
        f"DESCRIPTION:{escape('Programa e informació: ' + url)}",
        f"URL:{url}",
        "TRANSP:TRANSPARENT",
        "END:VEVENT",
    ]


def main() -> None:
    events = FESTES + SUMMER_SLUGS
    if len(events) != 80 or len({event[3] for event in events}) != len(events):
        raise ValueError("The source list must produce 80 unique festa entries.")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//GCal Festes Majors//CA", "CALSCALE:GREGORIAN", "X-WR-CALNAME:Festes Majors de Barcelona"]
    for event in events:
        lines.extend(event_lines(*event))
    lines.append("END:VCALENDAR")
    OUTPUT.write_bytes(("\r\n".join(fold(line) for line in lines) + "\r\n").encode("utf-8"))


if __name__ == "__main__":
    main()
