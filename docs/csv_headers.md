# Locked CSV Headers (v1)

These CSV headers (including column order) are LOCKED as part of the court artifact contract.

## eld_duty_status.csv
event_id,event_time_utc,event_type,status,lat,lon,location_source,odometer_miles,engine_hours,record_origin,notes_present

## gps_trace.csv
point_time_utc,lat,lon,speed_mph,heading_degrees,source

## safety_events.csv
event_id,event_time_utc,event_type,severity,metric,amount,lat,lon,location_source,source

## vehicle_state.csv
snapshot_time_utc,odometer_miles,engine_hours,fuel_percent,engine_rpm,speed_mph,dtc_codes_present,source

## 02_Evidence_Inventory.csv
evidence_type,source_system,capture_window_start_utc,capture_window_end_utc,status,captured_at_utc,artifact_id,filename,sha256,unavailable_reason_code,unavailable_reason_detail

## 03_Chain_of_Custody.csv
custody_time_utc,actor_type,actor_id,action,artifact_id,filename,detail
