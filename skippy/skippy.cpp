// Created by Thierry Tran
// Created on 13 July 2022
// Code for a game where main character is skipping obstacles


#include "raylib.h"
#include <stdlib.h>

struct AnimData{
    Rectangle rec;
    Vector2 pos;
    int frame;
    float updateTime;
    float runningTime;
};

bool isOnGround(AnimData data, int windowHeight){
    return data.pos.y <= windowHeight-data.rec.height;
}

AnimData animation(AnimData data, float dT ,int sizeFrame){
    data.runningTime += dT;
    if(data.runningTime>=data.updateTime){
        data.runningTime = 0.0;
        data.rec.x = data.frame*data.rec.width;
        data.frame++;

        if(data.frame>sizeFrame){
            data.frame = 0;
        }
    }
    return data;
}

void drawBackground(Texture2D background, float &bgX, float dT, float speed){
    bgX -= speed * dT;
    if(bgX <= -background.width*2){
        bgX = 0.0;
    }
    Vector2 bg1Pos = {bgX,0.0};
    Vector2 bg2Pos = {bgX + background.width*2,0.0};

    DrawTextureEx(background, bg1Pos, 0.0, 2.0, WHITE);
    DrawTextureEx(background, bg2Pos, 0.0, 2.0, WHITE);
}


Texture2D imageToTexture2D(char pathImage[], int width=0, int height=0, bool heightAsParam=false){
    Image raw = LoadImage(pathImage);
    if(heightAsParam){
        int newWidth = height * raw.width / raw.height;
        ImageResize(&raw, newWidth, height);
    }
    else{
        int newHeight = width * raw.height / raw.width;;
        ImageResize(&raw, width, newHeight);
    }
    Texture2D finalTexture = LoadTextureFromImage(raw);
    return finalTexture;
}

int randIntgerInRange(int min, int max){
    int randInt = min + (rand() % static_cast<int>(max - min + 1));
    return randInt;
}


void restartGame(KeyboardKey first_key, KeyboardKey second_key){
    // bool gameActive = true
    if(IsKeyDown(first_key)){
        //reset some variables
        //game function
    }
    else if(IsKeyDown(second_key)){
        // bool gameActive = false
        //close window
    }
}

void gameLogic(){
    // all game function
}

/*in main function, do while function gameActive*/

int main(){

    // Parameters for initial windows
    const float windowDimensions[2] = {512, 380};
    char windowTitle[] = "Skippy Bob";
    InitWindow(windowDimensions[0], windowDimensions[1], windowTitle);

    // Load sound effects
    InitAudioDevice();
    Sound jumpSound = LoadSound("sounds/jump.wav");
    Sound excitedSound = LoadSound("sounds/excited.wav");
    Sound sadSound = LoadSound("sounds/sad.wav");


    // Load background textures
    Texture2D background = imageToTexture2D("textures/background.png", 0, 192, true);
    Texture2D midground = imageToTexture2D("textures/midground.png", 0, 192, true);

    // Load character and create strcuture to hold character variables
    Texture2D bob = imageToTexture2D("textures/bob.png", 0, 60, true);
    AnimData bobData{{0.0, 0.0, static_cast<float>(bob.width / 6.0), static_cast<float>(bob.height)},
                        {windowDimensions[0] / 2 - bobData.rec.width / 2, windowDimensions[1] - bobData.rec.height - 800},
                        0, static_cast<float>(1.0 / 12.0), 0};

    // Load fire sprite
    Texture2D fire = LoadTexture("textures/fire_sprite.png");
    Texture2D nebula = LoadTexture("textures/nebula_sprite.png");
    Texture2D vortex = LoadTexture("textures/vortex_sprite.png");

    const int sizeObs = randIntgerInRange(10, 25);
    AnimData obstacles[sizeObs] = {};

    // Create various obstacles
    for(int i = 0; i<sizeObs; i++){
        obstacles[i] = {{0.0, 0.0, static_cast<float>(fire.width / 8.0), static_cast<float>(fire.height / 8.0)},
                        {windowDimensions[0] + 300 + i * (randIntgerInRange(200, 500)), windowDimensions[1] - fire.height / 8},
                        0, static_cast<float>(1.0 / randIntgerInRange(9, 12)), 0};
    }

    // Create variables for game logic
    float bgX{};
    float mgX{};
    bool endSound = true;
    int velocity = 0;
    const int gravity = 1000; //in pixels/s/s
    float finishLine = obstacles[sizeObs - 1].pos.x;
    int obsVel = -200; //obs velocity in pixels/seconds
    bool isInAir = false;
    const int jumpVel = -600; //in pixels/s/s
    bool collision = false;
    float bobLife = 100;

    SetTargetFPS(60);

    while(!WindowShouldClose()){

        BeginDrawing();
        ClearBackground(WHITE);

        float dT = GetFrameTime(); //time since last frame

        drawBackground(background, bgX, dT,20.0);
        drawBackground(midground, mgX, dT,40.0);

        if(isOnGround(bobData, windowDimensions[1])){
            velocity += gravity * dT;
            isInAir = true;
        }
        else{
            velocity = 0;
            isInAir = false;
        }

        if(IsKeyPressed(KEY_SPACE) && !isInAir){
            velocity += jumpVel;
            PlaySound(jumpSound);      
        }


        for(int i = 0; i<sizeObs; i++){
            obstacles[i].pos.x += obsVel*dT*(rand() % 2+1);
        }

        bobData.pos.y += velocity*dT;

        finishLine += obsVel * dT;

        if(!isInAir){   
            bobData = animation(bobData,dT,5);
        }

        for(int i = 0; i<sizeObs; i++){
            obstacles[i] = animation(obstacles[i], dT, 7);
            for(AnimData obs:obstacles){
                float pad = 50.0;
                Rectangle obsRec{obs.pos.x+pad, obs.pos.y+pad, obs.rec.width-2*pad, obs.rec.height-2*pad};
                Rectangle bobRec{bobData.pos.x, bobData.pos.y, bobData.rec.width, bobData.rec.height};

                if (CheckCollisionRecs(obsRec, bobRec)){
                    bobLife -= 0.40;
                    if (bobLife<0){
                        collision = true;
                    }
                    else{
                        DrawText("Ouch!", windowDimensions[0]/4, windowDimensions[1]/2, 50, RED);
                    }
                }
            }

            if(collision){
                DrawText("Game Over!\n Press 'N' to restart", windowDimensions[0]/4, windowDimensions[1]/2, 50, RED);
                if(endSound){
                    endSound = false;
                    PlaySound(sadSound);
                }
                if(IsKeyDown(KEY_N)){
                    main();
                }
            }
            else if(bobData.pos.x >= finishLine){
                DrawText("Bob wins!\nYeeepeeee!", windowDimensions[0]/4, windowDimensions[1]/2, 50, WHITE);
                if(endSound){
                    endSound = false;
                    PlaySound(excitedSound);
                }
            }
            else{
                for(int i = 0; i<sizeObs; i++){
                    if(i%2 == 0){
                        DrawTextureRec(fire, obstacles[i].rec, obstacles[i].pos,WHITE);
                    }
                    else if((i-1)%3 == 0){
                        DrawTextureRec(vortex, obstacles[i].rec, obstacles[i].pos,WHITE);
                    }
                    else{
                        DrawTextureRec(nebula, obstacles[i].rec, obstacles[i].pos,WHITE);
                    }
                }
            }
        }
        
        DrawTextureRec(bob, bobData.rec, bobData.pos, WHITE);

        EndDrawing();
    }

    UnloadTexture(bob);
    UnloadTexture(fire);
    UnloadTexture(background);
    UnloadTexture(midground);
    UnloadSound(jumpSound);
    UnloadSound(excitedSound);
    UnloadSound(sadSound);
    CloseAudioDevice();
    CloseWindow();

}

//TODO: add oups sound, change sound for happy, add restart option