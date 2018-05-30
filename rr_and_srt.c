#include<stdio.h>
void rr();
void srt();
int count,j,flag=0,time_quantum; 
int at[10],bt[10],rt[10],endTime,i,smallest;
int remain=0,n,time,wait_time=0,turnaround_time=0,smallest;
int main()
{   
printf("Enter no of Processes : ");
	scanf("%d",&n);
    for(i=0;i<n;i++)
    {
        printf("Enter arrival time for Process P%d : ",i+1);
        scanf("%d",&at[i]);
        printf("Enter burst time for Process P%d : ",i+1);
        scanf("%d",&bt[i]);
        rt[i]=bt[i];
    }
	int op;
    printf("enter choice  1.SRT  \t 2.RR \t 3.EXIT");
    scanf("%d",&op); 
    	if(op==1)
    	 srt();
      	   else if(op==2)
     		 rr();
     	else
      exit(0);
    printf("\n\nProcess\t|Turnaround Time| Waiting Time\n\n");
    printf("\n\nAverage waiting time = %f\n",wait_time*1.0/n);
	printf("Average Turnaround time = %f",turnaround_time*1.0/n);
	return 0;
}
void srt() 
{
rt[9]=9999;
    for(time=0;remain!=n;time++)
    {
        smallest=9;
        for(i=0;i<n;i++)
        {
            if(at[i]<=time && rt[i]<rt[smallest] && rt[i]>0)
            {
                smallest=i;
            }
        }
        rt[smallest]--;
        if(rt[smallest]==0)
        {
            remain++;
            endTime=time+1;
            printf("\nP[%d]\t|\t%d\t|\t%d",smallest+1,endTime-at[smallest],endTime-bt[smallest]-at[smallest]);
            wait_time+=endTime-bt[smallest]-at[smallest];
            turnaround_time+=endTime-at[smallest];
        }
    }
}
void rr()
{
	remain=n; 
	rt[count]=bt[count]; 
	printf("Enter Time Quantum:\t"); 
   scanf("%d",&time_quantum); 
   for(time=0,count=0;remain!=0;) 
   { 
    if(rt[count]<=time_quantum && rt[count]>0) 
    { 
      time+=rt[count]; 
      rt[count]=0; 
      flag=1; 
    } 
    else if(rt[count]>0) 
    { 
      rt[count]-=time_quantum; 
      time+=time_quantum; 
    } 
    if(rt[count]==0 && flag==1) 
    { 
      remain--; 
      printf("P[%d]\t|\t%d\t|\t%d\n",count+1,time-at[count],time-at[count]-bt[count]); 
      wait_time+=time-at[count]-bt[count]; 
      turnaround_time+=time-at[count]; 
      flag=0; 
    } 
    if(count==n-1) 
      count=0; 
    else if(at[count+1]<=time) 
      count++; 
    else 
      count=0; 
  } 
}


