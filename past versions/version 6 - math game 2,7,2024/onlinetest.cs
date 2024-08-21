int[] rainWeek = new int[] { 7, 8, 0, 4, 3, 8, 1 };


int lowestRainfall = rainWeek[0];
for (i = 0; i < rainWeek.length; i++) 
{ 
   int val = rainWeek[i]

   if (val != 0 && val < lowestRainfall)
      {
         lowestRainfall = val
      }
}