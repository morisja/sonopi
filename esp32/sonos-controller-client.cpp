#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define ROWS 5
#define COLS 24
#define INITVOL 50
#define SERVER_ADDRESS "192.168.0.223"
#define SERVER_PORT "5001"

class CommDriver {
  // This will talk to the sonos server hosted elsewhere
  private:
    int rows=ROWS;
  public:
    CommDriver() {
      // Use 'this->' to make the difference between the
      // 'pin' attribute of the class and the 
      // local variable 'pin' created from the parameter.
      init();
    }

    void init() {
        return;
    }
    void start_playlist(){
      printf("start playlist");
    }
    void playpause(){
      printf("play pause");
    }
    void next(){
      printf("next");
    }
    void prev(){
      printf("prev");
    }
}; // don't forget the semicolon at the end of the class


class ScreenDriver {
  // This will manage the tft with TTGO specific call
  private:
    int rows=ROWS;
    int cols=COLS;
    char prefixes[5][5]={ "","","","",""};
    char values[5][256]={ "","","","",""};
  public:
    ScreenDriver() {
      // Use 'this->' to make the difference between the
      // 'pin' attribute of the class and the 
      // local variable 'pin' created from the parameter.
      init();
    }

    void init() {
        return;
    }
    void setprefix(int idx, char *val){
      strcpy(prefixes[idx],val);      
    }
    void setvalue(int idx, char *val){
      strcpy(values[idx],val);      
    }

    void render(){
      for (int n=0;n<5;n++){
        printf("%s%s\n",prefixes[n],values[n]);        
      }      
    }
}; // don't forget the semicolon at the end of the class



class ScreenChooser {
  private:
    int pos=0;
    char prefixes[ROWS][5]={ "---:","---:",">>>:","---:","---:"};
    char values[ROWS][256]={ "","","","",""};
    char all_playlists[10][256] = {"","","queen","ac/dc","bowie","robbie gill","turkuaz","the daily","",""};
    ScreenDriver *sd;
    CommDriver *cd;
  public:
    long int id=0;
    ScreenChooser(CommDriver* cd1, ScreenDriver* sd1) {
      // Use 'this->' to make the difference between the
      // 'pin' attribute of the class and the 
      // local variable 'pin' created from the parameter.
      sd=sd1;
      cd=cd1;
      init();
    }
    void init() {
        id=random();
        return;
    }
    void scroll(int increment){
      int newpos=pos+increment;
      if(  newpos >= 0 && newpos <= sizeof(all_playlists)){
        pos=newpos;
      }
    }
    int scroll_select(){
      return pos;
    }    
    void render(){
      int i;
      int plidx;
      for (i=0;i<ROWS;i++){
        sd->setprefix(i,prefixes[i]);
      }
      for (i=0;i<ROWS;i++){
        plidx=pos+i;
        sd->setvalue(i,all_playlists[plidx]);
      }
      sd->render();
    }

}; // don't forget the semicolon at the end of the class


class ScreenDefault {
  private:
    int vol=INITVOL;
    char prefixes[ROWS][5]={ "    ","Vol:","Now:","PL :","   "};
    char values[ROWS][256]={ "","","","",""};
    ScreenDriver *sd;
    CommDriver *cd;
  public:
    long int id=0;
    ScreenDefault(CommDriver* cd1, ScreenDriver* sd1) {
      // Use 'this->' to make the difference between the
      // 'pin' attribute of the class and the 
      // local variable 'pin' created from the parameter.
      sd=sd1;
      cd=cd1;
      init();
    }
    void init() {
        id=random();
        return;
    }
    void scroll(int increment){
      int newvol=vol+increment;
      if(  newvol >= 0 && newvol  <=100){
        vol=newvol;
      }
    }
    void scroll_select(){
      return;
    }    
    void playpause(){
      cd->playpause();
      return;
    }    
    void next(){
      cd->next();
      return;
    }    
    void prev(){
      cd->prev();
      return;
    }    
    void set_volstring(char *c){
      strcpy(c,"[ volstring ]");
    }    
    void set_playingstring(char *c){
      strcpy(c,"playingstring");
    }    
    void render(){
      int i;
      set_volstring(values[1]);
      set_playingstring(values[2]);
      for (i=0;i<ROWS;i++){
        sd->setprefix(i,prefixes[i]);
      }
      for (i=0;i<ROWS;i++){
        sd->setvalue(i,values[i]);
      }
      sd->render();
    }

}; // don't forget the semicolon at the end of the class

class SonosApp {
  private:
    int rows=ROWS;
    //0=default, 1=chooser
    int current=0;
    ScreenChooser* sc;
    ScreenDefault* sd;
  public:
    SonosApp(ScreenDefault* sd1, ScreenChooser* sc1) {
      // Use 'this->' to make the difference between the
      // 'pin' attribute of the class and the 
      // local variable 'pin' created from the parameter.
      sd=sd1;
      sc=sc1;
      init();
    }

    void init() {
        return;
    }
    void scroll_select(){
      if (current == 0 ){
        current=1;
        sc->render();        
      }
      else if (current==1){
        current=0;
        sd->render();
      }
    }
    void scroll(int n){
      if (current ==0 ){
        //
      }
      else if (current == 1){
        sc->scroll(n);
      }
    }

    void render(){
      if (current ==0 ){
        sd->render();
      }
      else if (current == 1){
        sc->render();
      }
    }
}; // don't forget the semicolon at the end of the class


CommDriver cd2;
int main(void){
    CommDriver cd;
    ScreenDriver sd;
    ScreenDefault sdd(&cd,&sd);
    ScreenChooser sc(&cd,&sd);
    SonosApp sa(&sdd,&sc);
    sa.render();
    printf("\n");
    sa.scroll_select();
    sa.render();
    printf("\n");
    sa.scroll(1);
    sa.render();
    printf("\n");
    
}


