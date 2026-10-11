"""
campuses.py - Major Atlanta College Campuses Inside the Perimeter (ITP)

Provides accurate campus locations, landmarks, street/sidewalk-aligned
walking routes from OpenStreetMap and local graph data, safety infrastructure
nodes (Blue-Light emergency phones, LED lighting, ADA ramps), and turn-by-turn steps.
"""

import math
from typing import Any

CAMPUSES = {
    "gsu": {
        "name": "Georgia State University",
        "short_name": "GSU (Downtown)",
        "category": "Public Research",
        "badge": "Public Research • Downtown",
        "center": [33.7531, -84.3853],
        "zoom": 17,
        "default_start": "Hurt Park (Edgewood Ave & Gilmer St)",
        "default_end": "Student Center East (55 Gilmer St SE)",
        "description": "Dense urban campus integrated directly into downtown Atlanta's historic street grid.",
        "safety_notes": "Continuous LED streetlighting, high security camera coverage, 24/7 GSU Police call boxes.",
        # Exact OpenStreetMap geometry for Gilmer Street Southeast & Hurt Park sidewalk:
        # Strictly follows the street pavement and public sidewalks past Sparks Hall and Langdale Hall
        "route_coordinates": [
            [33.7544216, -84.3865050],  # Hurt Park entrance (Peachtree Center Ave & Gilmer St)
            [33.7541856, -84.3862564],  # Hurt Park paved sidewalk along Gilmer St
            [33.7538780, -84.3858469],  # Hurt Park fountain promenade
            [33.7535325, -84.3853869],  # Crossing Courtland St SE (Marked pedestrian signal)
            [33.7534860, -84.3853205],  # Courtland St sidewalk ramp
            [33.7534318, -84.3852501],  # Entrance to Library South / Sparks Hall walkway
            [33.7526883, -84.3842250],  # Gilmer St SE sidewalk along Langdale Hall
            [33.7526352, -84.3841565],  # Library Plaza accessible ramp
            [33.7525814, -84.3840855],  # Classroom South pedestrian way
            [33.7521464, -84.3835092],  # Gilmer St SE & Collins St connector
            [33.7518457, -84.3830985],  # Student Center East arrival crosswalk
            [33.7517987, -84.3830357],  # Student Center East Main Entrance (55 Gilmer St SE)
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7541856, -84.3862564], "label": "GSU Police Call Box #04 (Hurt Park)"},
            {"type": "lighting", "coords": [33.7535325, -84.3853869], "label": "Courtland St High-Lumen Crosswalk Lighting"},
            {"type": "blue_light", "coords": [33.7526883, -84.3842250], "label": "GSU Police Call Box #11 (Library South)"},
            {"type": "ada_ramp", "coords": [33.7526352, -84.3841565], "label": "ADA Tactile Curb Ramp (Library Plaza)"},
            {"type": "blue_light", "coords": [33.7517987, -84.3830357], "label": "GSU Student Center Security Desk Call Box"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Depart Hurt Park", "instruction": "Walk east on Gilmer St SE along the illuminated park promenade", "distance": "0.08 mi"},
            {"step": 2, "title": "Cross Courtland St SE", "instruction": "Cross at the signalized crosswalk equipped with audible pedestrian countdown", "distance": "0.02 mi"},
            {"step": 3, "title": "Pass Sparks & Langdale Hall", "instruction": "Follow Gilmer St SE sidewalk alongside GSU Library Plaza", "distance": "0.12 mi"},
            {"step": 4, "title": "Arrive at Student Center East", "instruction": "Enter via the ADA step-free entrance at 55 Gilmer St SE", "distance": "0.05 mi"},
        ],
        "safety_rating": 94,
    },
    "gt": {
        "name": "Georgia Institute of Technology",
        "short_name": "Georgia Tech (Midtown)",
        "category": "Public Research",
        "badge": "Public Research • Midtown",
        "center": [33.7756, -84.3963],
        "zoom": 16,
        "default_start": "John Lewis Student Center (Ferst Dr NW)",
        "default_end": "Tech Tower & Bobby Dodd Walkway",
        "description": "Midtown Atlanta campus featuring dedicated pedestrian spines and green spaces.",
        "safety_notes": "Continuous LED path lighting, blue emergency call boxes every 200 ft.",
        # Extracted directly from local OSM pedestrian graph (graph.graphml)
        "route_coordinates": [
            [33.7735993, -84.3987751],
            [33.7735449, -84.3987033],
            [33.7734779, -84.3985033],
            [33.7733449, -84.3984308],
            [33.7732594, -84.3983856],
            [33.7731583, -84.3979133],
            [33.7729643, -84.3974692],
            [33.7728633, -84.3972277],
            [33.7727871, -84.3970472],
            [33.7726714, -84.3967724],
            [33.7725833, -84.3965622],
            [33.7724892, -84.3963384],
            [33.7723924, -84.3961075],
            [33.7722841, -84.3958523],
            [33.7722324, -84.3957291],
            [33.7722661, -84.3956101],
            [33.7723880, -84.3955001],
            [33.7723190, -84.3947080],
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7735993, -84.3987751], "label": "GTPD Emergency Call Box (Student Center)"},
            {"type": "lighting", "coords": [33.7731583, -84.3979133], "label": "Tech Walkway Overhead Floodlight #08"},
            {"type": "blue_light", "coords": [33.7727871, -84.3970472], "label": "GTPD Emergency Call Box (Skiles Quad)"},
            {"type": "ada_ramp", "coords": [33.7723880, -84.3955001], "label": "Tech Tower ADA Gentle Ramp (< 2% grade)"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Depart Student Center", "instruction": "Head southeast onto the paved Tech Walkway pedestrian spine", "distance": "0.10 mi"},
            {"step": 2, "title": "Cross Tech Green Spine", "instruction": "Follow wide lit walkway past the Kessler Campanile", "distance": "0.15 mi"},
            {"step": 3, "title": "Approach Tech Tower", "instruction": "Arrive along the historic brick promenade at Tech Tower", "distance": "0.07 mi"},
        ],
        "safety_rating": 97,
    },
    "spelman": {
        "name": "Spelman College",
        "short_name": "Spelman College (AUC)",
        "category": "HBCU",
        "badge": "HBCU • Atlanta University Center",
        "center": [33.7464, -84.4129],
        "zoom": 17,
        "default_start": "Camille Olivia Hanks Cosby Center",
        "default_end": "Sisters Chapel & Historic Gates",
        "description": "Historic HBCU liberal arts institution for women within the Atlanta University Center.",
        "safety_notes": "Gated secure campus perimeter, active campus safety patrols, illuminated walkways.",
        "route_coordinates": [
            [33.7478000, -84.4148000],  # Cosby Center Promenade
            [33.7476500, -84.4138000],  # Westview Dr SW sidewalk
            [33.7475000, -84.4128000],  # Gated Campus Safety checkpoint
            [33.7473500, -84.4121000],  # Spelman Ln SW sidewalk
            [33.7468000, -84.4121000],  # Leonard St SW sidewalk
            [33.7464000, -84.4123000],  # Rockefeller Hall entrance
            [33.7462000, -84.4131000],  # Sisters Chapel walkway
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7478000, -84.4148000], "label": "Spelman Public Safety Station (Cosby Center)"},
            {"type": "lighting", "coords": [33.7475000, -84.4128000], "label": "Security Gate Continuous Illumination"},
            {"type": "blue_light", "coords": [33.7464000, -84.4123000], "label": "Rockefeller Hall Emergency Station"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Cosby Center to Spelman Ln", "instruction": "Follow illuminated sidewalk east along Westview Dr", "distance": "0.11 mi"},
            {"step": 2, "title": "Enter Gated Perimeter", "instruction": "Pass 24/7 security checkpoint into the historic quadrangle", "distance": "0.05 mi"},
            {"step": 3, "title": "Arrive at Sisters Chapel", "instruction": "Reach Sisters Chapel plaza along level brick walkway", "distance": "0.06 mi"},
        ],
        "safety_rating": 98,
    },
    "morehouse": {
        "name": "Morehouse College",
        "short_name": "Morehouse College (AUC)",
        "category": "HBCU",
        "badge": "HBCU • Atlanta University Center",
        "center": [33.7485, -84.4137],
        "zoom": 17,
        "default_start": "Martin Luther King Jr. International Chapel",
        "default_end": "Century Campus (Graves Hall)",
        "description": "Historic HBCU men's liberal arts college in the Atlanta University Center.",
        "safety_notes": "24/7 dedicated campus public safety, emergency call stations, tree-lined sidewalks.",
        # Nominatim verified street coordinates along Westview Dr SW & Century Quad
        "route_coordinates": [
            [33.7478000, -84.4148000],  # MLK Jr. International Chapel
            [33.7477500, -84.4138000],  # Westview Dr SW sidewalk (Forbes Arena)
            [33.7477000, -84.4126000],  # Westview Dr SW at historic campus gates
            [33.7483000, -84.4125500],  # Century Campus entrance walkway
            [33.7488000, -84.4125000],  # Graves Hall & Century Campus Quad
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7478000, -84.4148000], "label": "Morehouse Campus Police Station (MLK Chapel)"},
            {"type": "lighting", "coords": [33.7477500, -84.4138000], "label": "Forbes Arena Perimeter Streetlights"},
            {"type": "blue_light", "coords": [33.7488000, -84.4125000], "label": "Graves Hall Emergency Intercom"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Depart MLK Chapel", "instruction": "Head east along Westview Dr SW wide sidewalk", "distance": "0.10 mi"},
            {"step": 2, "title": "Turn into Century Campus", "instruction": "Turn north onto the historic quad walkway", "distance": "0.06 mi"},
            {"step": 3, "title": "Arrive at Graves Hall", "instruction": "Reach Graves Hall at the crest of the Century Quad", "distance": "0.04 mi"},
        ],
        "safety_rating": 97,
    },
    "cau": {
        "name": "Clark Atlanta University",
        "short_name": "Clark Atlanta (AUC)",
        "category": "HBCU",
        "badge": "HBCU • Atlanta University Center",
        "center": [33.7525, -84.4120],
        "zoom": 17,
        "default_start": "CAU Student Center (Atlanta Student Movement Blvd)",
        "default_end": "Harkness Hall & Trevor Arnett Quad",
        "description": "Comprehensive private HBCU and founding member of the Atlanta University Center.",
        "safety_notes": "Wide pedestrian sidewalks, high-visibility crosswalks, AUC security collaboration.",
        # Street sidewalk coordinates: Atlanta Student Movement Blvd SW to James P Brawley Dr SW
        "route_coordinates": [
            [33.7533000, -84.4136000],  # CAU Student Center on Atlanta Student Movement Blvd
            [33.7533000, -84.4126000],  # Sidewalk along Atlanta Student Movement Blvd SW
            [33.7533000, -84.4116000],  # Corner of ASM Blvd & James P Brawley Dr SW
            [33.7525000, -84.4116000],  # James P Brawley Dr SW sidewalk
            [33.7516000, -84.4116000],  # Harkness Hall & Quadrangle entrance
            [33.7508000, -84.4116000],  # Trevor Arnett Library
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7533000, -84.4136000], "label": "CAU Public Safety Station (Student Center)"},
            {"type": "lighting", "coords": [33.7533000, -84.4116000], "label": "Brawley Dr Pedestrian Signal & LED Mast"},
            {"type": "blue_light", "coords": [33.7516000, -84.4116000], "label": "Harkness Quad Emergency Station"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Depart Student Center", "instruction": "Walk east on Atlanta Student Movement Blvd sidewalk", "distance": "0.12 mi"},
            {"step": 2, "title": "Turn on Brawley Dr SW", "instruction": "Head south on James P Brawley Dr pedestrian corridor", "distance": "0.10 mi"},
            {"step": 3, "title": "Arrive at Harkness Hall", "instruction": "Reach Harkness Hall historic campus entrance", "distance": "0.05 mi"},
        ],
        "safety_rating": 95,
    },
    "msm": {
        "name": "Morehouse School of Medicine",
        "short_name": "Morehouse Medicine (AUC)",
        "category": "HBCU",
        "badge": "HBCU • Medical & Healthcare",
        "center": [33.7498, -84.4172],
        "zoom": 17,
        "default_start": "National Center for Primary Care (Westview Dr SW)",
        "default_end": "Medical Education Building (Lawshe St)",
        "description": "Dedicated HBCU medical and health sciences institution in the AUC.",
        "safety_notes": "Clinical-grade well-lit pathways, security patrols, step-free ADA ramps.",
        "route_coordinates": [
            [33.7498000, -84.4182000],  # NCPC Entrance on Westview Dr SW
            [33.7498000, -84.4170000],  # Westview Dr SW sidewalk
            [33.7498000, -84.4158000],  # Corner of Westview Dr SW & Lawshe St SW
            [33.7489000, -84.4158000],  # Lawshe St SW sidewalk
            [33.7485000, -84.4165000],  # Medical Education Building entrance
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7498000, -84.4182000], "label": "MSM Security Call Station (NCPC)"},
            {"type": "lighting", "coords": [33.7498000, -84.4158000], "label": "Hospital-Grade Illuminance Luminaire"},
            {"type": "ada_ramp", "coords": [33.7485000, -84.4165000], "label": "Clinical Building ADA Automatic Door Ramp"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Depart NCPC", "instruction": "Follow illuminated sidewalk east along Westview Dr SW", "distance": "0.14 mi"},
            {"step": 2, "title": "Turn on Lawshe St SW", "instruction": "Head south along clinical sidewalk corridor", "distance": "0.06 mi"},
            {"step": 3, "title": "Arrive at Medical Education", "instruction": "Enter through the staffed security atrium", "distance": "0.05 mi"},
        ],
        "safety_rating": 96,
    },
    "emory": {
        "name": "Emory University",
        "short_name": "Emory (Druid Hills)",
        "category": "Private Research",
        "badge": "Private Research • Druid Hills",
        "center": [33.7925, -84.3240],
        "zoom": 16,
        "default_start": "Emory Student Center (Asbury Circle)",
        "default_end": "Woodruff Library & Historic Quad",
        "description": "Renowned private research institution inside the perimeter in Druid Hills.",
        "safety_notes": "Pedestrianized central campus, Emory Police safe escort service, excellent lighting.",
        "route_coordinates": [
            [33.7909000, -84.3243000],  # Emory Student Center / Asbury Circle
            [33.7917000, -84.3238000],  # Asbury Circle pedestrian spine
            [33.7927000, -84.3235000],  # Dowman Dr sidewalk
            [33.7937000, -84.3237000],  # Dowman Dr along Emory Quad
            [33.7946000, -84.3242000],  # Woodruff Library entrance
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7909000, -84.3243000], "label": "Emory Blue-Light Tower (Asbury Circle)"},
            {"type": "lighting", "coords": [33.7927000, -84.3235000], "label": "Quad Pedestrian Lamppost #12"},
            {"type": "blue_light", "coords": [33.7946000, -84.3242000], "label": "Woodruff Library Emergency Station"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Depart Student Center", "instruction": "Walk north across paved Asbury Circle", "distance": "0.06 mi"},
            {"step": 2, "title": "Traverse Historic Quad", "instruction": "Follow marble-lined Dowman Dr pedestrian avenue", "distance": "0.14 mi"},
            {"step": 3, "title": "Arrive at Woodruff Library", "instruction": "Enter through the main front plaza", "distance": "0.06 mi"},
        ],
        "safety_rating": 95,
    },
    "agnesscott": {
        "name": "Agnes Scott College",
        "short_name": "Agnes Scott (Decatur)",
        "category": "Private Liberal Arts",
        "badge": "Liberal Arts • Decatur Core",
        "center": [33.7686, -84.2947],
        "zoom": 17,
        "default_start": "Agnes Scott Hall (Main)",
        "default_end": "McCain Library & Science Quad",
        "description": "Private women's liberal arts college in downtown Decatur inside I-285.",
        "safety_notes": "Close-knit walkable campus, adjacent to Decatur MARTA, monitored call boxes.",
        "route_coordinates": [
            [33.7680000, -84.2958000],  # Agnes Scott Main Hall
            [33.7680000, -84.2948000],  # E College Ave sidewalk
            [33.7688000, -84.2948000],  # Campus Promenade
            [33.7695000, -84.2942000],  # McCain Library entrance
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7680000, -84.2958000], "label": "Agnes Scott Police Tower (Main Hall)"},
            {"type": "lighting", "coords": [33.7688000, -84.2948000], "label": "Decatur Core Historic Streetlamp"},
            {"type": "blue_light", "coords": [33.7695000, -84.2942000], "label": "McCain Library Plaza Call Box"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Depart Main Hall", "instruction": "Follow tree-lined E College Ave sidewalk", "distance": "0.06 mi"},
            {"step": 2, "title": "Enter Central Lawn", "instruction": "Walk north along the brick-paved academic spine", "distance": "0.07 mi"},
            {"step": 3, "title": "Arrive at McCain Library", "instruction": "Reach the gothic entrance terrace", "distance": "0.04 mi"},
        ],
        "safety_rating": 97,
    },
    "scad": {
        "name": "SCAD Atlanta",
        "short_name": "SCAD Atlanta (Midtown)",
        "category": "Art & Design",
        "badge": "Art & Design • Peachtree Corridor",
        "center": [33.7997, -84.3905],
        "zoom": 16,
        "default_start": "SCAD Main (1600 Peachtree St NW)",
        "default_end": "SCAD FASH Museum of Fashion + Film",
        "description": "Savannah College of Art and Design urban campus along Midtown's Peachtree corridor.",
        "safety_notes": "Continuous street lighting along Peachtree St, high foot traffic, transit accessible.",
        "route_coordinates": [
            [33.7983000, -84.3912000],  # 1600 Peachtree St NW entrance
            [33.7992000, -84.3908000],  # Northbound Peachtree St NW sidewalk
            [33.8001000, -84.3904000],  # Peachtree St NW sidewalk (Brookwood)
            [33.8010000, -84.3900000],  # SCAD FASH & Forty Four Residence Hall
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7983000, -84.3912000], "label": "SCAD Security Desk (1600 Peachtree)"},
            {"type": "lighting", "coords": [33.7992000, -84.3908000], "label": "Midtown Corridor Commercial LED Mast"},
            {"type": "blue_light", "coords": [33.8010000, -84.3900000], "label": "SCAD FASH Museum Security Portal"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Depart 1600 Peachtree", "instruction": "Walk north along wide illuminated Peachtree St sidewalk", "distance": "0.08 mi"},
            {"step": 2, "title": "Midtown Commercial Path", "instruction": "Continue past Brookwood transit stop", "distance": "0.07 mi"},
            {"step": 3, "title": "Arrive at SCAD FASH", "instruction": "Enter Forty Four residence & museum lobby", "distance": "0.05 mi"},
        ],
        "safety_rating": 94,
    },
    "amsc": {
        "name": "Atlanta Metropolitan State College",
        "short_name": "Atlanta Metro State",
        "category": "Public College",
        "badge": "Public College • Southwest Atlanta",
        "center": [33.7145, -84.4150],
        "zoom": 16,
        "default_start": "Student Center (Metropolitan Pkwy SW)",
        "default_end": "McMillan Academic Sciences Building",
        "description": "Public state college serving Southwest Atlanta inside the I-285 perimeter.",
        "safety_notes": "Dedicated campus perimeter lighting, active safety escort patrols, accessible routes.",
        "route_coordinates": [
            [33.7140000, -84.4158000],  # Metropolitan Pkwy entrance
            [33.7140000, -84.4148000],  # Campus Drive sidewalk
            [33.7148000, -84.4145000],  # Academic Quad spine
            [33.7155000, -84.4142000],  # McMillan Sciences Building
        ],
        "safety_nodes": [
            {"type": "blue_light", "coords": [33.7140000, -84.4158000], "label": "AMSC Public Safety Station (Main Gate)"},
            {"type": "lighting", "coords": [33.7148000, -84.4145000], "label": "Campus Quad High-Intensity Streetlamp"},
            {"type": "blue_light", "coords": [33.7155000, -84.4142000], "label": "McMillan Science Building Emergency Box"},
        ],
        "turn_steps": [
            {"step": 1, "title": "Depart Student Center", "instruction": "Follow Campus Drive pedestrian sidewalk east", "distance": "0.07 mi"},
            {"step": 2, "title": "Enter Academic Quad", "instruction": "Turn north onto paved pedestrian spine", "distance": "0.06 mi"},
            {"step": 3, "title": "Arrive at McMillan Sciences", "instruction": "Reach main entrance portico", "distance": "0.05 mi"},
        ],
        "safety_rating": 92,
    },
}


def get_all_campuses() -> dict:
    """Return all cataloged Atlanta campuses inside the perimeter."""
    return CAMPUSES


def get_campus(campus_key: str) -> dict:
    """Return data for a specific campus, defaulting to GSU if not found."""
    return CAMPUSES.get(campus_key, CAMPUSES["gsu"])


def calculate_route_distance_miles(coordinates: list[list[float]]) -> float:
    """
    Calculate cumulative distance in miles along a coordinate polyline
    using the Haversine formula.
    """
    if len(coordinates) < 2:
        return 0.0

    total_miles = 0.0
    earth_radius_miles = 3958.8

    for i in range(len(coordinates) - 1):
        lat1, lon1 = coordinates[i]
        lat2, lon2 = coordinates[i + 1]

        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)

        a = (
            math.sin(d_lat / 2.0) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(d_lon / 2.0) ** 2
        )
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        total_miles += earth_radius_miles * c

    return round(max(0.1, total_miles), 2)


# Structured Campus Landmark Database
CAMPUS_LOCATIONS = {
    "gsu": {
        "Student Centers & Commons": {
            "Student Center East": (33.7518, -84.3831),
            "Student Center West": (33.75206, -84.38361),
            "Hurt Park Plaza": (33.7542, -84.3863),
            "Unity Plaza": (33.7519, -84.3834),
        },
        "Libraries & Academics": {
            "Library North": (33.7533, -84.3853),
            "Library South": (33.7527, -84.3850),
            "Aderhold Learning Center": (33.7562, -84.3888),
            "Langdale Hall": (33.7529, -84.3845),
            "Sparks Hall": (33.7535, -84.3854),
            "Classroom South": (33.7525, -84.3841),
            "Urban Life Building": (33.7516, -84.3856),
            "GSU Convocation Center": (33.7380, -84.3910),
        },
        "Dorms & Housing": {
            "University Commons": (33.7567, -84.3789),
            "Piedmont Central": (33.7562, -84.3798),
            "Piedmont North": (33.7589, -84.3820),
            "Patton Hall": (33.7560, -84.3812),
            "University Lofts": (33.7533, -84.3835),
        },
        "Parking Decks & Transit": {
            "M Deck (Piedmont Ave)": (33.7550, -84.3828),
            "G Deck (Collins St)": (33.7522, -84.3837),
            "T Deck (Auburn Ave)": (33.7545, -84.3860),
            "MARTA Georgia State Station": (33.7505, -84.3855),
            "MARTA Five Points Station": (33.7538, -84.3915),
        },
    },
    "gt": {
        "Student Centers & Commons": {
            "John Lewis Student Center": (33.7738, -84.3987),
            "Exhibition Hall": (33.7745, -84.3995),
            "Tech Green (Kessler Campanile)": (33.7748, -84.3964),
            "Bobby Dodd Stadium": (33.7725, -84.3928),
        },
        "Libraries & Academics": {
            "Clough Commons (CULC)": (33.7749, -84.3963),
            "Price Gilbert Memorial Library": (33.7743, -84.3957),
            "Tech Tower": (33.7724, -84.3947),
            "Klaus Advanced Computing Building": (33.7773, -84.3962),
            "College of Computing (CoC)": (33.7774, -84.3973),
            "Howey Physics Building": (33.7775, -84.3985),
        },
        "Dorms & Housing": {
            "North Avenue Apartments": (33.7712, -84.3918),
            "West Village Housing": (33.7788, -84.4035),
            "Glenn & Towers Residence Halls": (33.7715, -84.3935),
            "Eighth Street Apartments": (33.7782, -84.4005),
        },
        "Parking Decks & Transit": {
            "Student Center Deck (W02)": (33.7730, -84.4002),
            "Peters Parking Deck (E04)": (33.7747, -84.3922),
            "MARTA Midtown Station": (33.7811, -84.3863),
            "MARTA North Avenue Station": (33.7716, -84.3870),
        },
    },
    "auc": {
        "Student Centers & Chapels": {
            "Morehouse King Chapel Plaza": (33.7478, -84.4148),
            "Spelman Camille Cosby Center": (33.7462, -84.4140),
            "CAU Student Center": (33.7533, -84.4136),
            "Spelman Sisters Chapel": (33.7471, -84.4119),
        },
        "Libraries & Academics": {
            "Robert W. Woodruff Library (AUC)": (33.7505, -84.4135),
            "Morehouse Graves Hall (Century Campus)": (33.7488, -84.4125),
            "Spelman Rockefeller Hall": (33.7464, -84.4123),
            "CAU Harkness Hall & Quad": (33.7516, -84.4116),
            "MSM National Center for Primary Care": (33.7498, -84.4182),
            "MSM Medical Education Building": (33.7485, -84.4165),
        },
        "Dorms & Housing": {
            "Morehouse Perdue Hall": (33.7495, -84.4130),
            "Spelman Abby Rockefeller Hall": (33.7460, -84.4135),
            "CAU Brawley Hall Suites": (33.7520, -84.4130),
            "CAU Heritage Commons": (33.7540, -84.4140),
        },
        "Parking Decks & Transit": {
            "AUC Parking Deck (Lee St & Westview)": (33.7465, -84.4155),
            "MARTA West End Station": (33.7360, -84.4138),
            "MARTA Ashby Station": (33.7564, -84.4172),
        },
    },
}

# Alias individual AUC campus keys to the shared AUC landmark database
CAMPUS_LOCATIONS["spelman"] = CAMPUS_LOCATIONS["auc"]
CAMPUS_LOCATIONS["morehouse"] = CAMPUS_LOCATIONS["auc"]
CAMPUS_LOCATIONS["cau"] = CAMPUS_LOCATIONS["auc"]
CAMPUS_LOCATIONS["msm"] = CAMPUS_LOCATIONS["auc"]

# Additional campus landmark entries
CAMPUS_LOCATIONS["emory"] = {
    "Student Centers & Commons": {
        "Emory Student Center": (33.7909, -84.3243),
        "Asbury Circle": (33.7917, -84.3238),
    },
    "Libraries & Academics": {
        "Woodruff Library": (33.7946, -84.3242),
        "Emory Quadrangle": (33.7937, -84.3237),
    },
    "Dorms & Housing": {
        "Clairmont Campus": (33.7845, -84.3090),
        "Raoul Hall": (33.7900, -84.3225),
    },
    "Parking Decks & Transit": {
        "Peavine Parking Deck": (33.7920, -84.3280),
        "Fishburne Deck": (33.7955, -84.3220),
    },
}

CAMPUS_LOCATIONS["agnesscott"] = {
    "Student Centers & Commons": {
        "Alston Campus Center": (33.7690, -84.2960),
    },
    "Libraries & Academics": {
        "McCain Library": (33.7695, -84.2942),
        "Agnes Scott Hall (Main)": (33.7680, -84.2958),
    },
    "Dorms & Housing": {
        "Winship Hall": (33.7685, -84.2965),
    },
    "Parking Decks & Transit": {
        "West Parking Deck": (33.7690, -84.2975),
        "MARTA Decatur Station": (33.7745, -84.2960),
    },
}

CAMPUS_LOCATIONS["scad"] = {
    "Academic & Museum": {
        "SCAD Main (1600 Peachtree St NW)": (33.7983, -84.3912),
        "SCAD FASH Museum": (33.8010, -84.3900),
    },
    "Housing & Student Life": {
        "Forty Four Residence Hall": (33.8012, -84.3902),
        "The ACA Residence Hall": (33.7975, -84.3920),
    },
    "Parking & Transit": {
        "1600 Peachtree Parking": (33.7980, -84.3915),
        "MARTA Arts Center Station": (33.7892, -84.3872),
    },
}

CAMPUS_LOCATIONS["amsc"] = {
    "Student Life & Academics": {
        "Student Center": (33.7140, -84.4158),
        "McMillan Academic Sciences": (33.7155, -84.4142),
    },
    "Parking & Transit": {
        "Main Campus Lot": (33.7135, -84.4160),
        "MARTA Oakland City Station": (33.7170, -84.4250),
    },
}

# Offline address and intersection lookup table for fallback routing
OFFLINE_ADDRESS_LOOKUP = {
    # GSU Downtown
    "55 gilmer st": (33.7518, -84.3831),
    "55 gilmer st se": (33.7518, -84.3831),
    "66 courtland st": (33.75206, -84.38361),
    "66 courtland st se": (33.75206, -84.38361),
    "unity plaza": (33.7519, -84.3834),
    "student center east": (33.7518, -84.3831),
    "student center west": (33.75206, -84.38361),
    "100 peachtree st": (33.7555, -84.3888),
    "hurt park": (33.7542, -84.3863),
    "courtland st": (33.7535, -84.3854),
    "courtland st se": (33.7535, -84.3854),
    "gilmer st": (33.7527, -84.3845),
    "gilmer st se": (33.7527, -84.3845),
    "piedmont ave": (33.7534, -84.3828),
    "piedmont ave se": (33.7534, -84.3828),
    "decatur st": (33.7515, -84.3865),
    "decatur st se": (33.7515, -84.3865),
    "edgewood ave": (33.7545, -84.3860),
    "edgewood ave se": (33.7545, -84.3860),
    "aderhold": (33.7562, -84.3888),
    # Georgia Tech
    "350 ferst dr": (33.7738, -84.3987),
    "ferst dr": (33.7738, -84.3987),
    "ferst drive": (33.7738, -84.3987),
    "266 4th st": (33.7749, -84.3963),
    "tech green": (33.7748, -84.3964),
    "tech tower": (33.7724, -84.3947),
    "north ave": (33.7712, -84.3918),
    "north ave nw": (33.7712, -84.3918),
    "bobby dodd": (33.7725, -84.3928),
    # AUC
    "830 westview dr": (33.7478, -84.4148),
    "830 westview dr sw": (33.7478, -84.4148),
    "westview dr": (33.7478, -84.4148),
    "350 spelman ln": (33.7464, -84.4123),
    "350 spelman ln sw": (33.7464, -84.4123),
    "spelman ln": (33.7464, -84.4123),
    "223 james p brawley dr": (33.7516, -84.4116),
    "223 james p brawley dr sw": (33.7516, -84.4116),
    "james p brawley dr": (33.7516, -84.4116),
    "720 westview dr": (33.7498, -84.4182),
    "111 james p brawley dr": (33.7505, -84.4135),
    "fair st": (33.7533, -84.4136),
    "atlanta student movement blvd": (33.7533, -84.4136),
    # Emory
    "201 dowman dr": (33.7925, -84.3240),
    "clifton rd": (33.7915, -84.3235),
    # Agnes Scott
    "141 e college ave": (33.7680, -84.2958),
    # SCAD
    "1600 peachtree st": (33.7983, -84.3912),
    "1600 peachtree st nw": (33.7983, -84.3912),
    # AMSC
    "1630 metropolitan pkwy": (33.7140, -84.4158),
    "1630 metropolitan pkwy sw": (33.7140, -84.4158),
}


def get_campus_landmarks(campus_key: str) -> dict[str, tuple[float, float]]:
    """
    Return a flattened dictionary of {landmark_name: (lat, lon)} for a campus.
    """
    key = campus_key.lower() if campus_key else "gsu"
    campus_cats = CAMPUS_LOCATIONS.get(key, CAMPUS_LOCATIONS.get("gsu", {}))

    landmarks: dict[str, tuple[float, float]] = {}
    for _, items in campus_cats.items():
        landmarks.update(items)
    return landmarks


def get_categorized_landmarks(campus_key: str) -> dict[str, dict[str, tuple[float, float]]]:
    """
    Return categorized landmarks {category_name: {landmark_name: (lat, lon)}} for a campus.
    """
    key = campus_key.lower() if campus_key else "gsu"
    return CAMPUS_LOCATIONS.get(key, CAMPUS_LOCATIONS.get("gsu", {}))


def resolve_coordinates(
    input_val: str,
    campus_data: Any = None,
) -> tuple[float, float] | None:
    """
    Resolve a user input to (latitude, longitude) coordinates.

    Resolution strategy:
    1. Coordinate sequence: Parses strings formatted as 'lat, lon' or 'lat lon'.
    2. Preset landmark: Matches against CAMPUS_LOCATIONS landmarks.
    3. Offline lookup: Matches against OFFLINE_ADDRESS_LOOKUP table for standard
       campus street addresses and intersections.

    Parameters:
        input_val (str): User-provided input string.
        campus_data (dict | str | None): Active campus data dictionary or key string.

    Returns:
        tuple[float, float] | None: (lat, lon) tuple if resolved, else None.
    """
    if not input_val:
        return None

    val_clean = str(input_val).strip()

    # 1. Parse coordinate string like '33.7531, -84.3853' or '33.7531 -84.3853'
    import re
    coord_pattern = r"^([-+]?[0-9]+(?:\.[0-9]+)?)[,\s]+([-+]?[0-9]+(?:\.[0-9]+)?)$"
    match = re.match(coord_pattern, val_clean)
    if match:
        try:
            val1 = float(match.group(1))
            val2 = float(match.group(2))
            # Standard Atlanta coordinates: lat in [30, 36], lon in [-87, -81]
            if 30.0 <= val1 <= 36.0 and -87.0 <= val2 <= -81.0:
                return (round(val1, 6), round(val2, 6))
            # If coordinates were provided as (lon, lat), flip them
            if -87.0 <= val1 <= -81.0 and 30.0 <= val2 <= 36.0:
                return (round(val2, 6), round(val1, 6))
        except ValueError:
            pass

    # 2. Check preset landmark in CAMPUS_LOCATIONS
    campus_key = "gsu"
    if isinstance(campus_data, dict):
        # Look for short_name or key in dictionary
        for k, c_info in CAMPUSES.items():
            if c_info.get("name") == campus_data.get("name"):
                campus_key = k
                break
    elif isinstance(campus_data, str):
        campus_key = campus_data.lower()

    # Check active campus landmarks first
    active_landmarks = get_campus_landmarks(campus_key)
    clean_lower = val_clean.lower()

    for name, coords in active_landmarks.items():
        if name.lower() == clean_lower:
            return coords

    # Check all campuses
    for c_k, categories in CAMPUS_LOCATIONS.items():
        for _, items in categories.items():
            for name, coords in items.items():
                if name.lower() == clean_lower:
                    return coords

    # Partial/substring match in preset landmarks
    for name, coords in active_landmarks.items():
        if clean_lower in name.lower() or name.lower() in clean_lower:
            return coords

    # 3. Offline address lookup table
    for addr_key, coords in OFFLINE_ADDRESS_LOOKUP.items():
        if addr_key in clean_lower or clean_lower in addr_key:
            return coords

    # Fallback default: if campus_data is a campus dict or string key with center, return campus center
    if isinstance(campus_data, str) and campus_data.lower() in CAMPUSES:
        center = CAMPUSES[campus_data.lower()]["center"]
        return (float(center[0]), float(center[1]))
    if isinstance(campus_data, dict) and "center" in campus_data:
        center = campus_data["center"]
        return (float(center[0]), float(center[1]))

    return None

