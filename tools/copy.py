#!/usr/bin/env python3
"""The day's copy: 18 November 2026, as the wires reported it.

One lead package, three second-billed stories, fourteen cards, twenty-eight wire
briefs. Every figure was checked against the reporting named in `src` before it
went on the page; nothing here is invented.
"""

LEAD = {
    "region": "MIDDLE EAST",
    "desk": "IRAN WAR",
    "field": "WAR",
    "head": "Iran fires drones at Kuwait and Bahrain, and both answer",
    "deck": "Kuwait's air defences engaged \"hostile drone attacks\" before dawn and Bahrain "
            "intercepted \"several Iranian aerial attacks\", the third time this week. Iran's "
            "regular army claimed it had hit Patriot batteries and launch sites at Ali Al "
            "Salem; Kuwait did not confirm the claim and named no attacker. Neither state "
            "disclosed casualties. The salvo followed Tuesday's American strike on Qeshm "
            "Island, at the mouth of the Strait of Hormuz.",
    "src": "Reuters, AP, IRIB",
    "facts": [
        ("Kuwait", "The army's general staff said the explosions heard were its own "
                   "interceptors at work, and gave no number, location or damage. It did not "
                   "say who fired the drones."),
        ("Bahrain", "The defence force reported intercepting the attacks and the interior "
                    "ministry issued two shelter alerts before standing them down. The IRGC "
                    "said on Tuesday it had hit a radar at Sheikh Isa."),
        ("Qeshm", "A Hormozgan official confirmed the American strike and said it damaged no "
                  "housing, business or infrastructure on the island."),
    ],
}

SECOND = [
    {
        "region": "ASIA",
        "desk": "APEC",
        "field": "POLITICS",
        "head": "Xi greets Trump in Shenzhen on the eve of a three-way summit",
        "deck": "The first trilateral of the three nuclear powers meets on Thursday; arms "
                "control and Iran are on the table, Ukraine is not. Xi called the talks "
                "\"the most consequential of the decade\".",
        "src": "Reuters, AP",
    },
    {
        "region": "AMERICAS",
        "desk": "US SENATE",
        "field": "POLITICS",
        "head": "Peltola takes Alaska, and the Democrats take the Senate 56-44",
        "deck": "The AP called the last uncalled race at 10.19pm EST, after a count update put "
                "her on 50.1% to Dan Sullivan's 45.8%, past the threshold that avoids a "
                "ranked runoff.",
        "src": "AP",
    },
    {
        "region": "EUROPE",
        "desk": "UKRAINE WAR",
        "field": "WAR",
        "head": "Russia sends 141 drones at Ukraine in a single night",
        "deck": "Air defences downed or suppressed 126 of them, the air force said; the "
                "general staff counted 165 engagements, most of them on the Pokrovsk axis.",
        "src": "Ukrainian Air Force",
    },
]

CARDS = [
    {
        "region": "MIDDLE EAST",
        "desk": "GAZA",
        "field": "WAR",
        "head": "Board of Peace tells the UN the Gaza truce may collapse",
        "deck": "In its first annual report the board said Israel and Hamas have both fallen "
                "short, and that a ceasefire delivering nothing visible cannot be sustained.",
        "src": "AP",
    },
    {
        "region": "ASIA",
        "desk": "CYCLONE",
        "field": "DISASTER",
        "head": "Cyclone Akvan becomes a severe storm and sets course for Andhra",
        "deck": "The IMD expects landfall around noon on 20 November between Nellore and "
                "Visakhapatnam, at 120-130 km/h gusting to 145.",
        "src": "IMD",
    },
    {
        "region": "EUROPE",
        "desk": "ECONOMY",
        "field": "ECONOMY",
        "head": "UK inflation reaches a one-year high of 3.6% on fuel",
        "deck": "Motor fuel rose 33.2% on the year, the sharpest since July 2022, the ONS said. "
                "Bailey warned a long Iran war could force further rises.",
        "src": "ONS, Bank of England",
    },
    {
        "region": "AFRICA",
        "desk": "SUDAN",
        "field": "WAR",
        "head": "Amnesty: nine RSF drone strikes killed 37 civilians in El Obeid",
        "deck": "The rights group said the strikes hit homes, the power station, fuel stations "
                "and the main market, and should be tried as war crimes. The RSF denies it.",
        "src": "Amnesty International",
    },
    {
        "region": "AMERICAS",
        "desk": "HAITI",
        "field": "WAR",
        "head": "Salvadoran helicopters strike a gang leader's home in Canaan",
        "deck": "Bukele called the raid on Jeff Larose's house a gift to Haitians on the "
                "anniversary of Vertieres, a day after Port-au-Prince ratified a security pact.",
        "src": "Haitian Times, AP",
    },
    {
        "region": "ASIA",
        "desk": "BANGLADESH",
        "field": "ECONOMY",
        "head": "Garment protests shut 25 factories and block Dhaka's highways",
        "deck": "Police fired tear gas at workers on the Dhaka-Aricha road; about 300 have been "
                "arrested in the third week of a strike for a Tk 30,000 minimum wage.",
        "src": "AP, Daily Star",
    },
    {
        "region": "WORLD",
        "desk": "SPACE",
        "field": "SPACE",
        "head": "Voyager 1 becomes the first thing one light-day from Earth",
        "deck": "At 5.16am EST the probe passed 16.09 billion miles out, the distance light "
                "covers in a day, after 49 years, two months and eleven days of flight.",
        "src": "NASA JPL",
    },
    {
        "region": "AFRICA",
        "desk": "HORN OF AFRICA",
        "field": "WAR",
        "head": "Ethiopia and Eritrea mass troops along a 1,000km border",
        "deck": "Conflict monitors reported artillery and clashes near Badme last week, "
                "reviving fears of outright war between the two rivals.",
        "src": "Reuters, ACLED",
    },
    {
        "region": "OCEANIA",
        "desk": "SANCTIONS",
        "field": "POLITICS",
        "head": "Australia sanctions Daniella Weiss and her Nachala movement",
        "deck": "Penny Wong named three settlers and four bodies over illegal settlement and "
                "settler violence, with travel bans and asset freezes. Britain acted a day earlier.",
        "src": "DFAT",
    },
    {
        "region": "EUROPE",
        "desk": "THE HAGUE",
        "field": "JUSTICE",
        "head": "Thaci given 17 more months for obstructing his own trial",
        "deck": "The Kosovo Specialist Chambers found the former president had passed witness "
                "details to visitors in 2023. The term runs on top of his 25-year sentence.",
        "src": "KSC, AP",
    },
    {
        "region": "WORLD",
        "desk": "COP31",
        "field": "CLIMATE",
        "head": "COP31's draft deal urges an immediate shift off fossil fuels",
        "deck": "Australia's chairmanship put an 18-page text before Antalya calling for the "
                "transition and for adaptation finance to reach $120bn, with the gavel due Friday.",
        "src": "UNFCCC, Reuters",
    },
    {
        "region": "ASIA",
        "desk": "KASHMIR",
        "field": "WAR",
        "head": "LeT commander Lateef Bhat killed in a Kulgam encounter",
        "deck": "Security forces came under fire from a mosque in Zangalpora before dawn and "
                "killed the wanted militant inside, police said.",
        "src": "The Hindu",
    },
    {
        "region": "ASIA",
        "desk": "MONGOLIA",
        "field": "POLITICS",
        "head": "Mongolia's president resigns after a coal-contract revolt",
        "deck": "Ukhnaa Khurelsukh stood down after parliament refused his nominee for "
                "justice minister, ending a standoff that began with protests over a "
                "lucrative coal deal with China.",
        "src": "Reuters, Montsame",
    },
    {
        "region": "AFRICA",
        "desk": "CHAGOS",
        "field": "POLITICS",
        "head": "Mauritius gives Britain until December to surrender Chagos",
        "deck": "Port Louis said it would take the handover to the International Court of "
                "Justice if the treaty transferring sovereignty is not ratified this year.",
        "src": "AFP",
    },
]

BRIEFS = [
    ("Sanaa", "Government forces struck dozens of Houthi military sites; UNICEF says 64 children have been killed since September."),
    ("Taiz", "More than 800,000 people are cut off from aid after the Aden road closed, the UN said."),
    ("Kabul", "The UN released $18m from its emergency fund to reach 800,000 Afghans through the winter."),
    ("Geneva", "The WHO said resistance to last-resort antibiotics is now worse than it was in 2019."),
    ("Manila", "Trump and Marcos signed a trade and defence package; the Quad met at leader level for the first time in two years."),
    ("Prague", "Two trains collided outside the main station, injuring 46 people, four of them critically."),
    ("Belgrade", "A Serbian MiG-29 crashed near Stara Pazova and the pilot was killed, local media reported."),
    ("Kemerovo", "A military aircraft came down in Siberia with 19 people aboard; none survived."),
    ("Port Louis", "Mauritius gave Britain until December to hand over the Chagos Islands or face legal action."),
    ("Seoul", "The Kospi closed 2% higher as Asian markets recovered from the week's outages."),
    ("London", "Brent fell 1.4% to $91.82 a barrel as traders priced a shorter war premium."),
    ("Berlin", "Pistorius pledged further air-defence systems, guided missiles and F-16 munitions to Kyiv."),
    ("Brussels", "Lammy met EU counterparts to reset the post-Brexit defence relationship."),
    ("Warsaw", "Poland said it foiled a sabotage plot against rail freight bound for Ukraine."),
    ("Nairobi", "OHCHR counted 1,120 civilians killed by drones in Sudan in the first half of the year, 80% of conflict deaths."),
    ("Mexico City", "US and Mexican officials resumed trade talks after a week's pause."),
    ("Caracas", "Hegseth met Venezuela's interim leadership as US forces repositioned in the Caribbean."),
    ("Washington", "Rubio said the bank, airline and cloud failures were unrelated and found no hostile actor behind them."),
    ("Washington", "The NSA said a temporary degradation, not an attack, took its classified network down on Tuesday."),
    ("New York", "The FAA grounded flights again while engineers traced a router fault signed off minutes before it failed."),
    ("Houston", "A chemical plant explosion injured workers and shut a ship channel for the day."),
    ("Los Angeles", "A Six Flags coaster derailed, killing one rider and injuring several."),
    ("Ottawa", "Canada opened talks with Meta over news payments, a month before the act takes effect."),
    ("Sydney", "Tame Impala swept the ARIAs; \"human\" was named the word of the year."),
    ("Johannesburg", "South African inflation held at 5.2%, leaving room for a cut in January."),
    ("Madidi", "Researchers catalogued 99 bat species in the Bolivian park, a record for a single survey."),
    ("Dongola", "Archaeologists reached the floor of the old church at Old Dongola after four seasons."),
    ("Buenos Aires", "Argentina's Senate advanced the mining royalty bill over provincial objections."),
]

STATS = [
    ("16.09bn", "MILES OUT, VOYAGER 1"),
    ("141", "DRONES AT UKRAINE"),
    ("2,500", "TROOPS IN HAITI"),
    ("3.6%", "UK INFLATION"),
    ("145", "KM/H GUSTS, AKVAN"),
    ("56-44", "THE NEW SENATE"),
    ("37", "KILLED IN EL OBEID"),
]

FILED = 18
WIRE = 28
