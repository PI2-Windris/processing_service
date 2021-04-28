import simpful as sf
from datetime import datetime

def evaluate_eolic(wind, potency):
  FS = sf.FuzzySystem()
  # Wind and potency are both trapezoidal
  W_1 = sf.FuzzySet( points=[[0, 1.],  [2, 1.],  [3, 0]], term="low_wind" )
  W_2 = sf.FuzzySet( points=[[2.5, 0], [6, 1.], [15, 1], [20, 0]], term="ideal_wind" )
  W_3 = sf.FuzzySet( points=[[20.0, 0],  [25., 1.], [35, 1.]], term="high_wind" )

  P_1 = sf.FuzzySet( points=[[0, 1.],  [75, 1.],  [150, 0]], term="low_potency" )
  P_2 = sf.FuzzySet( points=[[125, 0], [400, 1.], [1000, 1], [1500, 0]], term="average_potency" )
  P_3 = sf.FuzzySet( points=[[1450, 0],  [2000, 1.], [2500, 1.]], term="high_potency" )

  FS.add_linguistic_variable("WIND", sf.LinguisticVariable( [W_1, W_2, W_3] ))
  FS.add_linguistic_variable("POT", sf.LinguisticVariable( [P_1, P_2, P_3] ))

  # consequents.
  FS.set_crisp_output_value("HEALTHY", 0)
  FS.set_crisp_output_value("UNHEALTHY", 1)

  # fuzzy rules.
  RULE1 = "IF (WIND IS high_wind) AND (POT IS low_potency)  THEN (HEALTH IS UNHEALTHY)"
  RULE2 = "IF (WIND IS ideal_wind) AND (POT IS low_potency)  THEN (HEALTH IS UNHEALTHY)"
  RULE3 = "IF (WIND IS ideal_wind) AND (POT IS average_potency)  THEN (HEALTH IS HEALTHY)"
  FS.add_rules([RULE1, RULE2, RULE3])

  # Set antecedents values, perform Sugeno inference and print output values.
  FS.set_variable("WIND", wind)
  FS.set_variable("POT", potency)

  health = FS.Sugeno_inference(['HEALTH'])
  return health_status(health['HEALTH'])

def evaluate_solar(temperature, potency):
  FS = sf.FuzzySystem()
  # Temperature and potency are both trapezoidal
  W_1 = sf.FuzzySet( points=[[0, 1.],  [5.0, 1.],  [20.0, 0]],          term="low_temp" )
  W_2 = sf.FuzzySet( points=[[15.0, 0], [20.0, 1.], [35.0, 1], [65.0, 0]], term="ideal_temp" )
  W_3 = sf.FuzzySet( points=[[20.0, 0],  [40., 1.], [80.0, 1.]],          term="high_temp" )

  P_1 = sf.FuzzySet( points=[[0, 1.],  [50, 1.],  [100, 0]],          term="low_potency" )
  P_2 = sf.FuzzySet( points=[[80, 0], [150, 1.], [400, 1], [500, 0]], term="average_potency" )
  P_3 = sf.FuzzySet( points=[[450.0, 0],  [600., 1.], [1000, 1.]],          term="high_potency" )

  FS.add_linguistic_variable("TEMP", sf.LinguisticVariable( [W_1, W_2, W_3] ))
  FS.add_linguistic_variable("POT", sf.LinguisticVariable( [P_1, P_2, P_3] ))

  # consequents.
  FS.set_crisp_output_value("HEALTHY", 0)
  FS.set_crisp_output_value("UNHEALTHY", 1)

  # fuzzy rules.
  RULE1 = "IF (TEMP IS high_temp) AND (POT IS low_potency)  THEN (HEALTH IS UNHEALTHY)"
  RULE2 = "IF (TEMP IS ideal_temp) AND (POT IS low_potency)  THEN (HEALTH IS UNHEALTHY)"
  RULE3 = "IF (TEMP IS ideal_temp) AND (POT IS average_potency)  THEN (HEALTH IS HEALTHY)"
  FS.add_rules([RULE1, RULE2, RULE3])

  # Set antecedents values, perform Sugeno inference and print output values.
  FS.set_variable("TEMP", temperature)
  FS.set_variable("POT", potency)

  health = FS.Sugeno_inference(['HEALTH'])
  return health_status(health['HEALTH'])

def health_status(value):
  status = dict({0: "Saudável", 1: "Não Saudável"})
  health = {
    "health_status": status[value],
    "evaluated_at":  datetime.now().isoformat()
  }
  return health

