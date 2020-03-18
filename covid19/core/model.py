from scipy.integrate import odeint


class SIR:
    def __init__(self, population, infected, recovered, beta, gamma):
        """
        This model calculates

        Based on https://github.com/DmitrySerg/COVID-19/blob/master/models/COVID-19.ipynb

        :param population: Total population
        :param infected: Initial number of infected individuals,
        :param recovered: Everyone else is susceptible to infection initially
        :param beta: number of contacts per day
        :param gamma: fraction of the infected group is recovered during any given day

        Contact rate, beta, and mean recovery rate, gamma, (in 1/days)
        """
        self.N = population
        self.I0 = infected
        self.R = recovered
        self.beta = beta
        self.gamma = gamma
        self.S0 = population - infected - recovered

    @staticmethod
    def _deriv(y, t, N, beta, gamma):
        """
        The SIR model differential equations

        :param y: [S, I, R] for current t_i (see constructor)
        :param t: t_i time
        :param beta: number of contacts per day
        :param gamma: fraction of the infected group is recovered during any given day

        :return dSdt, dIdt, dRdt: derivatives for S, I, R (see constructor)
        """
        S, I, R = y
        dSdt = -beta[int(t)] * S * I / N
        dIdt = beta[int(t)] * S * I / N - gamma * I
        dRdt = gamma * I
        return dSdt, dIdt, dRdt

    def run(self, days):
        """
        Running process of epidemic

        :param days:
        :return s, i, r after i days (see constructor)
        """
        # Initial conditions vector
        y0 = [self.S0, self.I0, self.R]
        # Integrating the SIR equations over the time grid, t
        t = list(range(0, days))
        # Getting results
        result = odeint(self._deriv, y0, t, args=(self.N, self.beta, self.gamma))
        s, i, r = result.T
        return s, i, r


class City:
    def __init__(self, name, population, infected, recovered):
        """

        :param name: city name
        :param population: city's population
        :param infected: infected peoples
        :param recovered: recovered peoples
        """
        self.name = name
        self.population = population
        self.infected = infected
        self.recovered = recovered

    def _sample_infected(self, n):
        # TODO: make it more realistic (maybe random sampled)
        # TODO: check if it sends more then exists
        return n * self.infected // self.population

    def _sample_recovered(self, n):
        # TODO: make it more realistic (maybe random sampled)
        # TODO: check if it sends more then exists
        return n * self.recovered // self.population

    def send_people(self, n):
        inf_t = self._sample_infected(n)
        rec_t = self._sample_recovered(n)
        self.infected -= inf_t
        self.recovered -= rec_t
        self.population -= n
        return inf_t, rec_t
