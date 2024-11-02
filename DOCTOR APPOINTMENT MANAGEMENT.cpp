#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_APPOINTMENTS 100
#define CONSOLE_WIDTH 80

// Structure to hold patient information
typedef struct {
    char firstName[50];
    char lastName[50];
    char contact[15];
    int ageGroup;
    char previousMedicalCondition[100];
    char appointmentType[20];
    int id;
    time_t arrivalTime;
    int burstTime;
    int waitTime;
    int finishTime;
} Patient;

// Global variables
Patient appointments[MAX_APPOINTMENTS];
int appointmentCount = 0;
int nextNormalCheckId = 1;
int nextEmergencyId = 1;

// Function to create an appointment
void createAppointment() {
    if (appointmentCount >= MAX_APPOINTMENTS) {
        printf("Appointment limit reached.\n");
        return;
    }

    Patient patient;

    // Taking personal information
    printf("Enter patient details:\n");
    printf("First name: ");
    scanf(" %49[^\n]", patient.firstName);
    printf("Last name: ");
    scanf(" %49[^\n]", patient.lastName);
    printf("Contact number: ");
    scanf(" %14[^\n]", patient.contact);

    // Age group selection
    printf("Select age group:\n");
    printf("1. 3 to 10\n2. 11 to 15\n3. 16 to 24\n4. 25 to 35\n5. 36 and above\n");
    printf("Enter your choice (1 to 5): ");
    scanf("%d", &patient.ageGroup);

    while (patient.ageGroup < 1 || patient.ageGroup > 5) {
        printf("Invalid choice. Enter a number between 1 and 5: ");
        scanf("%d", &patient.ageGroup);
    }

    // Previous medical condition
    printf("Enter previous medical condition (if any): ");
    scanf(" %99[^\n]", patient.previousMedicalCondition);

    // Appointment type selection
    int choice;
    printf("Select appointment type:\n1. Normal Check\n2. Emergency\n");
    printf("Enter your choice (1 or 2): ");
    scanf("%d", &choice);

    while (choice != 1 && choice != 2) {
        printf("Invalid choice. Enter 1 for Normal Check or 2 for Emergency: \n");
        scanf("%d", &choice);
    }

    if (choice == 1) {
        strcpy(patient.appointmentType, "Normal Check");
        patient.burstTime = 5;
        patient.id = nextNormalCheckId++;
    } else {
        strcpy(patient.appointmentType, "Emergency");
        patient.burstTime = 60;
        patient.id = nextEmergencyId++;
    }

    // Get current time as arrival time
    patient.arrivalTime = time(NULL);

    // Calculate wait and finish time
    if (appointmentCount == 0) {
        patient.waitTime = 0;
    } else {
        Patient lastPatient = appointments[appointmentCount - 1];
        patient.waitTime = lastPatient.finishTime - patient.arrivalTime;
    }
    patient.finishTime = patient.arrivalTime + patient.waitTime + patient.burstTime;

    // Insert patient based on priority
    if (strcmp(patient.appointmentType, "Emergency") == 0) {
        for (int i = appointmentCount; i > 0; i--) {
            appointments[i] = appointments[i - 1];
        }
        appointments[0] = patient;
    } else {
        appointments[appointmentCount] = patient;
    }
    appointmentCount++;

    // Confirmation message
    printf("Appointment created successfully!\nYour appointment ID is: %d\n", patient.id);
}

// Function to display all appointments
void listAppointments() {
    printf("All Appointments:\n");

    for (int i = 0; i < appointmentCount; i++) {
        Patient patient = appointments[i];

        // Convert arrivalTime and finishTime to readable format
        char arrivalTimeStr[20];
        strftime(arrivalTimeStr, sizeof(arrivalTimeStr), "%Y-%m-%d %H:%M:%S", localtime(&patient.arrivalTime));

        time_t finishTimeT = patient.finishTime;
        char finishTimeStr[20];
        strftime(finishTimeStr, sizeof(finishTimeStr), "%Y-%m-%d %H:%M:%S", localtime(&finishTimeT));
        printf("----------------------------------------------------------------------------------------------------------------------\n");
        printf("~ID: %d \t, Name: %s %s \t, Type: %s \t, Previous Medical Condition: %s \t, Arrival Time: %s \t,\n \n Wait Time: %d mins \t, Finish Time: %s \t \n",
               patient.id, patient.firstName, patient.lastName, patient.appointmentType,
               patient.previousMedicalCondition, arrivalTimeStr, patient.waitTime, finishTimeStr);
        printf("----------------------------------------------------------------------------------------------------------------------\n");  
    }
}

// Function to search a patient by ID
void searchAppointment() {
    int searchId;
    printf("Enter patient ID to search: ");
    scanf("%d", &searchId);

    int found = 0;
    for (int i = 0; i < appointmentCount; i++) {
        if (appointments[i].id == searchId) {
            Patient patient = appointments[i];
            printf("\nPatient Details:\n");
            printf("ID: %d, Name: %s %s, Type: %s, Contact: %s, Age Group: %d, Medical Condition: %s\n", 
                   patient.id, patient.firstName, patient.lastName, patient.appointmentType,
                   patient.contact, patient.ageGroup, patient.previousMedicalCondition);
            found = 1;
            break;
        }
    }
    if (!found) {
        printf("No appointment found with ID: %d\n", searchId);
    }
}

// Function to calculate and display average wait times
void displayAverageWaitTime() {
    int totalWaitNormal = 0, totalWaitEmergency = 0, countNormal = 0, countEmergency = 0;

    for (int i = 0; i < appointmentCount; i++) {
        if (strcmp(appointments[i].appointmentType, "Normal Check") == 0) {
            totalWaitNormal += appointments[i].waitTime;
            countNormal++;
        } else if (strcmp(appointments[i].appointmentType, "Emergency") == 0) {
            totalWaitEmergency += appointments[i].waitTime;
            countEmergency++;
        }
    }

    printf("\nAverage Waiting Times:\n");
    printf("Normal Check: %.2f mins\n", countNormal ? (double)totalWaitNormal / countNormal : 0.0);
    printf("Emergency: %.2f mins\n", countEmergency ? (double)totalWaitEmergency / countEmergency : 0.0);
}

// Main function
int main() {
    char choice;

    // Printing headers
    printf("\n----------------------\n");
    printf("  CPU SCHEDULING \n");
    printf("----------------------\n");
    printf("WELCOME TO DOCTOR'S APPOINTMENT SYSTEM\n\n");

    do {
    	printf("----------------------\n");
        printf("Menu:\n1. Create Appointment\n2. List Appointments\n3. Search Appointment\n4. Average Wait Time\n5. Exit\n");
        printf("Enter your choice: ");
        scanf(" %c", &choice);
        printf("------------------------------\n");
        
        switch (choice) {
            case '1':
                createAppointment();
                break;
            case '2':
                listAppointments();
                break;
            case '3':
                searchAppointment();
                break;
            case '4':
                displayAverageWaitTime();
                break;
            case '5':
                printf("Exiting program...\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != '5');

    return 0;
}

