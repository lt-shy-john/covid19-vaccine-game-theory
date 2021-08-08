class Vaccine:

    def __init__(self, name, dose, days, vaccine_type, cost, efficacy, alpha, beta, gamma, delta, phi):
        self.brand = name
        self.dose = dose
        self.days_to_next_dose = days
        self.type = vaccine_type
        self.cost = cost
        self.efficacy = efficacy
        self.alpha_V = alpha
        self.beta_V = beta
        self.gamma_V = gamma
        self.delta_V = delta
        self.phi_V = phi
