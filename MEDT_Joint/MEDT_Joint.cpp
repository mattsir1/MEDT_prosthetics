// MEDT_Joint.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include <iostream>
#include "..\JointINO\JointControlSystem.cpp"

//not functioning in test suite, arduino specific methods
void setCurrentAngle(int) {}; //do nothing
void servoWriteAngle(bool, int) {};

//grip types
#define GRIP_NONE       0
#define GRIP_FLAT       1
#define GRIP_MOUSE      2
#define GRIP_TRIPOD     3
#define GRIP_POINTER    4
#define GRIP_HOOK       5
#define GRIP_POWER      6
int GetGrip(float wrist_flex, float wrist_rot, float other, float index, float thumb) 
{
    if (wrist_rot == 0)
    {
        if (wrist_flex == 0)
        {
            if (75 < other < 80)
            {
                if (index < 80)
                {						//InRange(max=80, min=65, range=10)
                    if (65 < index < 75) 			//max is min+range -- actuation range
                    {
                        if (thumb == 0)                                
                            return GRIP_POWER;
                    }
                    //between 75 and 80
                    return GRIP_HOOK;
                }
                if (index == 0 && thumb == 0)                          
                    return GRIP_POINTER;
            }
            else if (35 < other < 40)
                if (35 < index < 40 && 35 < thumb < 40)                
                    return GRIP_TRIPOD;
            else if (other == 0 && index == 0 && thumb == 0)           
                return GRIP_MOUSE;
        }
        else if (80 < wrist_flex < 85)
            if (other == 0 && index == 0 && thumb == 0)                
                return GRIP_FLAT;
    }
    return GRIP_NONE;
}
int main()
{
    std::cout << "Beginning test suite...\n";
    //joint count, coefficients, cyclerate
    JointControlSystem* jcs = new JointControlSystem(5, new float[5] {0.5, 0.5, 0.5, 0.5, 0.5});// , 200.f);
    jcs->m_joints[0] = &JointControlSystem::Joint(0, 0.f, 0.f, 0, 360);
    jcs->m_joints[1] = &JointControlSystem::Joint(1, 0.f, 0.f, 0, 360);
    jcs->m_joints[2] = &JointControlSystem::Joint(2, 0.f, 0.f, 0, 360);
    jcs->m_joints[3] = &JointControlSystem::Joint(3, 0.f, 0.f, 0, 360);
    jcs->m_joints[4] = &JointControlSystem::Joint(4, 0.f, 0.f, 0, 360);

    float testingValues[][5]{
        {0,80,0,0,0},  //rot
        {1,0,0,0,0},    //flex
        {2,0,0,0,0},    //other  
        {3,0,0,0,0},    //index     
        {4,0,0,0,0},    //thumb     
    };
    for (int i = 0; i < 5; i++) //for each row
    {   
        jcs->UpdateStoredData(testingValues[i]);
        for (int j = 0; j < 5; j++) //for each column
        {
            std::cout << "Testing " << j << "\n";
            if (jcs->m_joints[j]->InRange(jcs))
            {
                float angle = jcs->m_joints[j]->GetDegrees(jcs); //
                std::cout << j << "In range\n";
            }
            else 
            {
                std::cout << j << "Out of range\n";
            }
        }
    }
    //after processing all points, get GRIP is called to return the resulting grip type
    std::cout << "Test suite completed...\n";
}
