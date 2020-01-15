# RAT - Reservoir Assessment Tool
This repository is dedicated to use for the Reservoir Assessment Tool (RAT)- A Global Reservoir Assessment Tool for Predicting Hydrologic Impact and Operating Pattern of Existing and Planned Reservoirs. The Reservoir Assessment Tool (RAT) represents a global and freely accessible system to monitor the operating pattern of world’s current and planned reservoirs and their impact on water availability. RAT is designed to address limitations faced by downstream stakeholders in developing regions of limited access to measurement data and upstream opaque transboundary reservoir policy. It is based on the core SASWE principle that ‘access to information on water is a fundamental right for all humans and nations.’ The development of RAT is always on-going. The developers do not accept any responsibility for wrongful application or faulty decision making based on RAT outputs. Users should read the key documentation on RAT (see to how to Cite) and use RAT at their own risk.

The repository divided into two subdirectories:
1) Frontend
2) Backend

# Frontend
The main window of the frontend is shown in figure 5 (beta version of the tool hosted at http://depts.washington.edu/saswe/rat_beta/). This frontend was developed from a freely-available template at https://html5up.net/forty and necessary changes made in HTML, CSS and JavaScript code as per the requirements. Currently, 1598 Dams from the GranD Database version 1.3 located in South America, Africa and South-East Asia are modeled operationally for monitoring reservoir dynamics and added to the RAT frontend interface. A major river network was added for user convenience to the GUI. Leaflet API (https://leafletjs.com/) used to visualize geoJSON formatted dam locations and river networks over base-map. Several types of base-maps (i.e., Google Satellite, Global Surface Water Dataset-GSWD) provided in the front-end to visualize administrative boundaries, water extents, and imagery information.  All the reservoir parameters (i.e., AEC curve, surface water extent, inflow, storage change, and outflow) were added to the frontend through an iframe. All of the HTML, CSS and JavaScript code for the iframe were developed from scratch. In figure 6, all of the above components are shown displayed the way they can appear on the RAT GUI.

# Backend
*The main script to process backedn datasets is RAT_backend.py. It has different modules, they are described below.*

1) retrievearea: used to generate the surface water extent timeseries from Landsat imageries in GEE  
Inputs: GranD reservoir polygons (users/nbiswas/grand1p3_reservoirs_saafseasia) and Landsat 8 imageries (LANDSAT/LC08/C01/T1_RT), both of the datasets made available in GEE.  
Outputs: Surface water extent area timeseries for each of the reservoirs and saved in the directory 'data/sarea/L8'  

2) areafiltering: used to filter out un-realistic estimations from surface area timeseries  
Inputs: output from (1)  
Outputs: Surface water extent area timeseries for each of the reservoirs and saved in the directory 'data/sarea/L8_modified'  

3) aecextraction: used to extract aec relationship in GEE from SRTM data  
Inputs: GranD reservoir polygons (users/nbiswas/grand1p3_reservoirs_saafseasia), SRTM Dem data (USGS/SRTMGL1_003) in GEE.  
Outputs: Area-Elevation coordinates for each of the reservoirs and saved in the directory 'data/aec'  

4) aecmodification: used to extrapolate area-elevation relationship from (2)  
Inputs: Area-Elevation coordinates for each of the reservoirs available in the directory 'data/aec'  
Outputs: Area-Elevation coordinates for each of the reservoirs and saved in the directory 'data/aec_modified'  

5) deltaS: used to calculate storage change from the area-elevation relationship mentioned in (3) and surface area timeseries mentioned in (1)  
Inputs: Outputs from (2) and (4)  
Outputs: Change in storage timeseries for each of the reservoirs and saved in the directory 'data/deltas'  

6) vicinflow: used to calculate reservoir inflow from the VIC hydrological Model  
Inputs: VIC-Route results output saved in 'Route_Output'  
Outputs: Inflow for each of the reservoirs and saved in the directory 'data/inflow'  

7) outflow: calcute reservoir outflow  
Inputs: Outputs from (5) and (6)  
Outputs: Outflow from each fo the reservoirs saved in the directory 'data/outflow'  

# Citation
The standard citation for this portal and data is “Biswas, N., Hossain, F., Lee, H., Bonnema, M., Jayasinghe, S., Basnayake, S. (2020) A Global Reservoir Assessment Tool for Predicting Hydrologic Impact and Operating Pattern of Existing and Planned Reservoirs, Environmental Modeling and Software."
# Contact
Nishan Kumar Biswas (http://students.washington.edu/nbiswas/ and nbiswas@uw.edu)
SASWE Research Group: www.saswe.net
