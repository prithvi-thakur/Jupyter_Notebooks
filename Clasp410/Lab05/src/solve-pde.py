######################################################
#
#   SNOWBALL EARTH
#
#   Author: Prithvi Thakur
#   Written in: Python v3.6.6
#   Last Modified: 11-20-2018
#
#   Clasp 410 Lab 5: Snowball earth
#                   Solve the pde
#                    
######################################################


# Import modules
import numpy as np
import os
import matplotlib.pyplot as plt
plt.ion()

# Path to save figures
path = '/Volumes/GoogleDrive/My Drive/Courses/coursework/Clasp410/Lab05/figs/'


# Global variables
Re = 6371e3     # Radius of earth
So = 1367       # Solar Flux
Cp = 4.2e6      # Heat Capacity of sea water
dz = 50         # Depth of mixed ocean layer
λ = 1e-2         # Thermal Diffusivity
ε = 0.595         # Emissivity
σ = 5.67e-8     # Steffan-Boltzmann constant
ρ = 1027        # Density of the ocean



# Define insolation setup
def insolation(Nx, φ, So):
    max_tilt = 23.5
    days_in_year = 365
    hours_in_day = 24
    zonal_degrees = 360
     
    dlong = 0.01    # use 1/100th of a degree in summing over latitudes
    total_solar = 0.0
    
    for hour in range(hours_in_day):
        hour_angle = zonal_degrees * (hour+1) /hours_in_day
        
        for longitude in range(int(zonal_degrees/dlong)):
            sun_angle = (longitude+1) - hour_angle
            total_solar += So* max(0.0, np.cos(np.pi*sun_angle/180)) 
    
    So = total_solar/(hours_in_day*zonal_degrees/dlong)
    
    # Initialize insolation to zero
    insolation = np.zeros(Nx)
    
    # Accumulate normalized insolation through an year
    for day in range(days_in_year):
        tilt = max_tilt*np.cos(2*np.pi*(day+1)/days_in_year)
    
        for j in range(Nx):
            zenith = min(φ[j]+tilt, 90.0)
            insolation[j] += np.cos(np.deg2rad(zenith))
    
    insolation = So*insolation/days_in_year
    
    return insolation

# Insolation ans copied from matlab
def insolation_m():
    Sy = np.array([36.3259,107.8738,176.1441,239.0623,294.7167,341.4163,\
            377.7422,402.5905,415.2064,415.2064,402.5905,377.7422,341.4163,\
            294.7167,239.0623,176.1441,119.7120,74.9634])
    return Sy


# Incoming long wave and shortwave radiation:
# added to the forcing term
def incoming_radiation(Sy, T, α):
    global ε, σ, ρ, dx, Cp, So
    
    f2 = (Sy*(1-α) - ε*σ*T**4)/(dz*Cp*ρ)

    f2[0] = 0
    f2[-1] = 0

    return f2


# Domain discretization
def domain(N):
    global Re
    Δφ = 180/N  # Latitude discretization
    φ = np.linspace((Δφ/2)-90, 90-(Δφ/2), N)
    h = (np.sin(np.deg2rad(φ + Δφ/2)) - np.sin(np.deg2rad(φ - Δφ/2)))*Re
    area = 2*np.pi*Re*h # of each latitude band
    Δy = np.pi*Re/N
    return φ, area, Δy

# General Finite Difference matrix
def fdm(N):
    K = (-2*np.eye(N) + np.diag(np.ones(N-1),k=1) + np.diag(np.ones(N-1),k=-1))
    return K

# Zero slope boundary condition: returns modified finite difference matrix
def boundary(K, Δy):
    # Set the first and last row to match the boundary conditions
    K[0,0] = -1
    K[0,1] = 1
    K[-1,-2] = 1
    K[-1,-1] = -1
    return K/(Δy**2)

# area forcing term
def forcing(T, area, Δy):
    # T_(i+1) - T_(i-1)
    tdiff = T[2::] - T[0:-2]
    
    # A_(i+1) - A_(i-1)
    Adiff = area[2::] - area[0:-2]

    # forcing
    f = tdiff*Adiff
    
    # Boundary Conditions: f = 0 at boundaries
    return np.hstack([0,f,0])/(area*4*Δy**2)


# Main function
def main():
    global Re , λ

    # Number of latitude bands: space discretization
    Nx = 18

    # Number of timesteps: time dicretization
    yr2sec = 365*24*60*60
    dt = 1*yr2sec; tmax = 20000*yr2sec
    Nt = int(tmax/dt)

    # Domain discretization
    φ, area, Δy = domain(Nx)
   
    # Finite difference matrix: second derivative
    Ko = fdm(Nx)
    K = boundary(Ko, Δy)

    y = Re*φ
    
    # Pre-allocate the unknown T
    T = np.zeros((Nx, Nt))

    # Initial condition
    T[:,0] = np.array([-47, -19, -11, 1, 9, 14, 19, 23, 25, 25, 23, 19, \
                        14, 9, 1, -11, -19, -47])

    #  T[:,0] = (-60)*np.ones(Nx)

    # Celsius to Kelvin
    T[:,0] = T[:,0] + 273
    # Solar Flux
    So = 1367
   
    # Question 5: simulations with initial temperature feedback

    # store the values of γ (solar multiplier) and final avg temp
    tmp = np.linspace(0.6,1.4,10)
    γ = np.hstack([tmp[:-1], tmp[::-1]])

    γ = [200.55]

    nos = len(γ)     # number of simulations
    Tavg = np.zeros(nos)
    ice_frac = np.zeros(nos)
    
    for sim_num in range(nos):
        So = γ[sim_num]*So

        # Insolation
        Sy = insolation(Nx, φ, So)
        
        # Albedo
        α = 0.3*np.ones(Nx) 
         
        # Time-step
        for j in range(1, Nt):
            
            # Area term
            f1 = forcing(T[:,j-1], area, Δy)
            
            # Change albedo according to temp.
            α[T[:,j-1] < 263] = 0.6
            α[T[:,j-1] > 263] = 0.3
            
            # Incoming radiation term
            f2 = incoming_radiation(Sy, T[:,j-1], α)

            L = np.eye(Nx) - dt*λ*K
            b = T[:,j-1] + dt*(λ*f1 + f2)

            T[:, j] = np.linalg.solve(L,b)
       
        # Plot only 100 points
        it = int(Nt/100)
        
        Tavg[sim_num] = glob_avg_temp(T-273, area)
        ice_frac[sim_num] = ice_fraction(T-273, area)

        tplot(T[:,0::it] - 273, Nx, sim_num)
        #  energy_check(T[:,0::it] - 273, area, tmax/yr2sec)
       
        # Update initial temperature for next simulation
        T[:,0] = T[:,-1].copy()

    plot_multiplier(Tavg, ice_frac, γ)
    return T, Tavg, ice_frac, γ

# Plot temperature isolines
def tplot(T, Nx, sim_num):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(T, np.linspace(-90,90,Nx), "k--", lw=0.4, alpha=0.4)
    ax.plot(T[:,0], np.linspace(-90,90,Nx), "k--", lw=1, label='Initial')
    ax.axvline(-10, label = "Ice threshold")

    ax.set_xlabel("Temperature (Celsius)")
    ax.set_ylabel("Latitude")
    ax.set_title(r"Temperature contours")
    ax.legend()
    filename = os.path.join(path, 'tcont_8'+str(sim_num)+'.png')
    plt.savefig(filename, dpi=300)
    plt.show()

# Diffusivity vs. global steady state 
def diff_plot(T, Nx):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(T, np.linspace(-90,90,Nx), "k--", lw=0.4)

    ax.set_xlabel("Global steady state temperature (K)")
    ax.set_ylabel("Latitude")
    ax.set_title("Q2 : Steady state temperature for different diffusivity (N=18 points)")
    filename = os.path.join(path, 'tdiff_q6.png')
    #  plt.savefig(filename, dpi=300)
    plt.show()

# Check if the energy is conserved
def energy_check(T, area, tmax):
    Tavg = np.zeros(T[0,:].size)
    for i in range(T[0,:].size):
        Tavg[i] = (T[:,i]*area).sum()/(area.sum())
    
    x_axis = np.linspace(0, tmax, Tavg.size)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x_axis, Tavg, ".")

    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Global avg. temperature (celsius)")
    ax.set_title("Global avg. temperature in time")
    filename = os.path.join(path, 'tavg_q5.png')
    #  plt.savefig(filename, dpi=300)
    plt.show()

# Calculate the final global avg. temperature
def glob_avg_temp(T, area):
    return (T[:,-1]*area).sum()/area.sum()

# Calculate fraction of planet covered with ice
def ice_fraction(T, area):
    return (area[T[:,-1] < -10]).sum()/area.sum()

# Plot avg. temp and ice fraction vs γ
def plot_multiplier(Tavg, ice_frac, γ):
    fig, ax1 = plt.subplots()
    color1 = 'tab:blue'
    ax1.set_xlabel("Solar multipler γ")
    ax1.set_ylabel("Fraction of planet covered with ice")
    ax1.plot(γ, ice_frac, 'o--', color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel("Global average temperature at steady state (Celsius)")
    ax2.plot(γ, Tavg, '*--', color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    plt.suptitle("Ice fraction and avg. temp as a function of solar multiplier")
    #  fig.tight_layout()
    plt.legend()
    filename = os.path.join(path, 'ratios_6.png')
    #  plt.savefig(filename, dpi=300)

T, Tavg, ice_frac, gamma = main()
