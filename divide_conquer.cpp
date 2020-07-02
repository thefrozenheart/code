/*
*/
#include<iostream>

void merge(int *ptr_array,int *temptr_array,int left, int mid,int right)
    {
        int i=left,j=mid+1,k=0;
        while (i<=mid & j<=right)
        {
            if(ptr_array[i]<=ptr_array[j])
            {
                temptr_array[k++]=ptr_array[i++];
            }
            else
            {
                temptr_array[k++]=ptr_array[j++];
            }
        }
        while (i<=mid)
        {
            /* code */
            temptr_array[k++]=ptr_array[i++];
        }
        while (j<=right)
        {
            /* code */
            temptr_array[k++]=ptr_array[j++];
        }

        k=0;
        
        while(left <= right){
            ptr_array[left++] = temptr_array[k++];
        }
    }
void sort(int *ptr_array,int *temptr_array,int left,int right)
    {
        // std::cout<<left<<right<<std::endl;
        if(left<right){
            int mid=(left+right)/2;
            sort(ptr_array,temptr_array,left,mid);
            sort(ptr_array,temptr_array,mid+1,right);
            merge(ptr_array,temptr_array,left,mid,right);
        }
    }

int main(){
    int length=7;
    int data[length]={7,6,5,4,3,2,1};
    int temp[length]={0};

    // merge(data,temp,0,0,1);
    sort(data,temp,0,length-1);

    for(int i=0;i<length;i++){
    std::cout<<temp[i]<<std::endl;
    }
    return 0;

}