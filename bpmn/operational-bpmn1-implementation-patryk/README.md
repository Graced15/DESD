# How to Run My BPMN

## Requirements
- Camunda 8 Run (8.10.9)
- Camunda Desktop Modeler
- Python 3

## 1. Start Camunda

Download Camunda 8 Run and put the `c8run-8.10.9` folder in Downloads.

Open Terminal and run:

```bash
cd ~/Downloads/c8run-8.10.9
./start.sh
```

Wait for Camunda to start.

## 2. Deploy Files

In Camunda Desktop Modeler, open and deploy these files from the `camunda` folder:

1. `sign_in_demo.form`
2. `product_details.form`
3. `operational-bpmn1-implementation-patryk.bpmn`

## 3. Start Python Worker

Open another Terminal and run:

```bash
cd ~/Desktop/operational-bpmn1-implementation-patryk/python
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export CAMUNDA_REST_ADDRESS="http://localhost:8080/v2"
export CAMUNDA_AUTH_STRATEGY=NONE
python main.py
```

Leave both Terminals open.

## 4. Test the BPMN

In Desktop Modeler, start a new instance with:

```json
{"accountExists": true}
```

Open http://localhost:8080/tasklist and complete the sign-in and product details tasks. Leave Organic unchecked.

Check the result at http://localhost:8080/operate.

Login: `demo` / `demo`

Organic certificate verification is not implemented yet.
