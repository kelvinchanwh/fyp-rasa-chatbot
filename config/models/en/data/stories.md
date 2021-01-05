
## fallback
- utter_unclear

## Story 1
* flight
    - utter_boarding
* inform{"location": "BCN"}
    - action_save_origin
    - slot{"from": "BCN"}
    - utter_destination
* inform{"location": "MUC"}
    - action_save_destination
    - slot{"to": "MUC"}
    - utter_date
* inform{"date": "20/06/2019"}
    - action_save_date
    - slot{"date": "20/06/2019"}
    - utter_confirm
* affirmation
    - action_get_flight
    - utter_check_another_one
* deny
    - utter_thanks
    - action_restart

## Stry 2-multiple steps
* flight
    - utter_boarding
* inform{"location": "CPT"}
    - action_save_origin
    - slot{"from": "CPT"}
    - utter_destination
* inform{"location": "BCN"}
    - action_save_destination
    - slot{"to": "BCN"}
    - utter_date
* inform{"date": "03/07/2019"}
    - slot{"date": "03/07/2019"}
    - action_save_date
    - slot{"date": "03/07/2019"}
    - utter_confirm
* affirmation
    - action_get_flight
    - utter_check_another_one
* affirmation
    - action_slot_reset
    - reset_slots
    - utter_boarding
* inform{"location": "BCN"}
    - action_save_origin
    - slot{"from": "BCN"}
    - utter_destination
* inform{"location": "MUC"}
    - action_save_destination
    - slot{"to": "MUC"}
    - utter_date
* inform{"date": "10/07/2019"}
    - slot{"date": "10/07/2019"}
    - action_save_date
    - slot{"date": "10/07/2019"}
    - utter_confirm
* affirmation
    - action_get_flight
    - utter_check_another_one
* deny
    - utter_thanks
    - action_restart

